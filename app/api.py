from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required, login_user
from .models import (
    Prompt,
    Language,
    Like,
    Favorite,
    User,
    PromptStatus,
    UserRole,
    Review,
    ReviewStatus,
)
from .auth import jwt_required, admin_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid
from mongoengine.queryset.visitor import Q

api = Blueprint("api", __name__)


def serialize_prompt(prompt, user_liked_prompts=None, user_favorited_prompts=None):
    """序列化 Prompt 对象为 JSON 格式"""
    try:
        # 如果传入了预加载的数据，使用预加载的数据
        is_liked = False
        is_favorited = False

        # 调试信息
        print(f"正在序列化提示: {prompt}")
        print(f"提示类型: {type(prompt)}")

        if isinstance(prompt, dict):
            # 确保_id存在
            if "_id" not in prompt:
                print("错误：提示对象中没有_id字段")
                return None

            author = prompt.get("author", {})
            language = prompt.get("language", {})

            # 调试信息
            print(f"作者信息: {author}")
            print(f"语言信息: {language}")

            if user_liked_prompts is not None:
                is_liked = str(prompt["_id"]) in user_liked_prompts
            if user_favorited_prompts is not None:
                is_favorited = str(prompt["_id"]) in user_favorited_prompts

            return {
                "id": str(prompt["_id"]),
                "title": prompt.get("title"),
                "content": prompt.get("content"),
                "status": prompt.get("status"),
                "author": (
                    {
                        "id": (
                            str(author["_id"]) if author and "_id" in author else None
                        ),
                        "name": author.get("name"),
                        "avatar_url": author.get("avatar_url"),
                    }
                    if author
                    else None
                ),
                "language": (
                    {
                        "id": (
                            str(language["_id"])
                            if language and "_id" in language
                            else None
                        ),
                        "name": language.get("name"),
                        "slug": language.get("slug"),
                    }
                    if language
                    else None
                ),
                "likes_count": prompt.get("likes_count", 0),
                "favorites_count": prompt.get("favorites_count", 0),
                "created_at": (
                    prompt.get("created_at").isoformat()
                    if prompt.get("created_at")
                    else None
                ),
                "is_liked": is_liked,
                "is_favorited": is_favorited,
            }
        else:
            if user_liked_prompts is not None:
                is_liked = str(prompt.id) in user_liked_prompts
            if user_favorited_prompts is not None:
                is_favorited = str(prompt.id) in user_favorited_prompts

            return {
                "id": str(prompt.id),
                "title": prompt.title,
                "content": prompt.content,
                "status": prompt.status,
                "author": (
                    {
                        "id": str(prompt.author.id),
                        "name": prompt.author.name,
                        "avatar_url": prompt.author.avatar_url,
                    }
                    if prompt.author
                    else None
                ),
                "language": (
                    {
                        "id": str(prompt.language.id),
                        "name": prompt.language.name,
                        "slug": prompt.language.slug,
                    }
                    if prompt.language
                    else None
                ),
                "likes_count": prompt.likes_count,
                "favorites_count": prompt.favorites_count,
                "created_at": prompt.created_at.isoformat(),
                "is_liked": is_liked,
                "is_favorited": is_favorited,
            }
    except Exception as e:
        print(f"序列化提示时出错: {str(e)}")
        print(f"提示对象: {prompt}")
        import traceback

        print(f"错误堆栈: {traceback.format_exc()}")
        return None


def serialize_user(user):
    """序列化 User 对象为 JSON 格式"""
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "role": user.role,
        "created_at": user.created_at.isoformat(),
    }


@api.route("/prompts", methods=["GET", "POST"])
def get_prompts():
    if request.method == "POST":
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Authentication required"}), 401

        try:
            # 从 Authorization 头中提取 token
            token = auth_header.split(" ")[1]
            # 验证 token
            user = User.verify_token(token)
            if not user:
                return jsonify({"message": "Invalid or expired token"}), 401
            # 登录用户
            login_user(user)
        except Exception as e:
            return jsonify({"message": "Invalid token format"}), 401

        data = request.get_json()

        if not all(key in data for key in ["title", "content", "language"]):
            return jsonify({"message": "Missing required fields"}), 400

        language = Language.objects(id=data["language"]).first()
        if not language:
            return jsonify({"message": "Invalid language"}), 400

        prompt = Prompt(
            title=data["title"],
            content=data["content"],
            language=language,
            author=current_user.id,
            status=PromptStatus.PUBLISHED,
        ).save()

        return (
            jsonify(
                {
                    "message": "Prompt created successfully",
                    "prompt": serialize_prompt(prompt),
                }
            ),
            201,
        )

    try:
        # 获取查询参数
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 12, type=int)  # 每页显示12个提示词
        language = request.args.get("language")
        prompt_type = request.args.get("type", "all")

        # 构建查询条件
        query = Q(status=PromptStatus.PUBLISHED)
        if language:
            lang = Language.objects(slug=language).first()
            if lang:
                query &= Q(language=lang.id)

        # 获取总数
        total = Prompt.objects(query).count()

        # 根据类型排序
        if prompt_type == "popular":
            prompts = Prompt.objects(query).order_by("-likes_count", "-created_at")
        else:
            prompts = Prompt.objects(query).order_by("-created_at")

        # 应用分页
        prompts = prompts.skip((page - 1) * per_page).limit(per_page)

        # 获取当前用户的点赞和收藏数据
        user_liked_prompts = set()
        user_favorited_prompts = set()
        if current_user.is_authenticated:
            user_liked_prompts = {
                str(like.prompt.id) for like in Like.objects(user=current_user.id)
            }
            user_favorited_prompts = {
                str(favorite.prompt.id)
                for favorite in Favorite.objects(user=current_user.id)
            }

        # 序列化提示词
        prompts_data = [
            serialize_prompt(prompt, user_liked_prompts, user_favorited_prompts)
            for prompt in prompts
        ]

        # 构建分页信息
        pagination = {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "has_prev": page > 1,
            "has_next": page * per_page < total,
        }

        return jsonify({"prompts": prompts_data, "pagination": pagination})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Failed to fetch prompts"}), 500


@api.route("/languages")
def get_languages():
    languages = Language.objects.order_by("-popularity")

    # 计算每个语言的提示词数量
    language_counts = {}
    for language in languages:
        language_counts[str(language.id)] = Prompt.objects(
            language=language, status=PromptStatus.PUBLISHED
        ).count()

    return jsonify(
        {
            "languages": [
                {
                    "id": str(lang.id),
                    "name": lang.name,
                    "slug": lang.slug,
                    "popularity": lang.popularity,
                    "prompts_count": language_counts[str(lang.id)],
                }
                for lang in languages
            ],
            "total_prompts": Prompt.objects(status=PromptStatus.PUBLISHED).count(),
        }
    )


@api.route("/prompts/<prompt_id>/like", methods=["POST"])
@jwt_required
def toggle_like(prompt_id):
    try:
        prompt = Prompt.objects(id=prompt_id).first_or_404()
        like = Like.objects(user=current_user.id, prompt=prompt_id).first()

        if like:
            like.delete()
            prompt.likes_count = max(0, prompt.likes_count - 1)
        else:
            Like(user=current_user.id, prompt=prompt_id).save()
            prompt.likes_count += 1

        prompt.save()

        return jsonify(
            {
                "message": "Like toggled successfully",
                "is_liked": like is None,
                "likes_count": prompt.likes_count,
            }
        )
    except Exception as e:
        return jsonify({"message": "Failed to toggle like", "error": str(e)}), 500


@api.route("/prompts/<prompt_id>/favorite", methods=["POST"])
@jwt_required
def toggle_favorite(prompt_id):
    try:
        prompt = Prompt.objects(id=prompt_id).first_or_404()
        favorite = Favorite.objects(user=current_user.id, prompt=prompt_id).first()

        if favorite:
            favorite.delete()
            prompt.favorites_count = max(0, prompt.favorites_count - 1)
        else:
            Favorite(user=current_user.id, prompt=prompt_id).save()
            prompt.favorites_count += 1

        prompt.save()

        return jsonify(
            {
                "message": "Favorite toggled successfully",
                "is_favorited": favorite is None,
                "favorites_count": prompt.favorites_count,
            }
        )
    except Exception as e:
        return jsonify({"message": "Failed to toggle favorite", "error": str(e)}), 500


@api.route("/prompts/<prompt_id>", methods=["GET"])
def get_prompt(prompt_id):
    prompt = Prompt.objects(id=prompt_id, status=PromptStatus.PUBLISHED).first_or_404()

    # 获取用户的点赞和收藏状态
    if current_user.is_authenticated:
        current_user.liked_prompts = {
            str(like.prompt.id) for like in Like.objects(user=current_user.id)
        }
        current_user.favorited_prompts = {
            str(fav.prompt.id) for fav in Favorite.objects(user=current_user.id)
        }

    return jsonify({"prompt": serialize_prompt(prompt)})


@api.route("/user/profile")
@login_required
def get_user_profile():
    return jsonify({"user": serialize_user(current_user)})


@api.route("/user/prompts")
@login_required
def get_user_prompts():
    prompts = Prompt.objects(author=current_user.id).order_by("-created_at")

    # 获取用户的点赞和收藏状态
    current_user.liked_prompts = {
        str(like.prompt.id) for like in Like.objects(user=current_user.id)
    }
    current_user.favorited_prompts = {
        str(fav.prompt.id) for fav in Favorite.objects(user=current_user.id)
    }

    return jsonify({"prompts": [serialize_prompt(p) for p in prompts]})


@api.route("/user/likes")
@login_required
def get_user_likes():
    liked_prompt_ids = [like.prompt.id for like in Like.objects(user=current_user.id)]
    prompts = Prompt.objects(id__in=liked_prompt_ids).order_by("-created_at")

    # 获取用户的点赞和收藏状态
    current_user.liked_prompts = {str(p.id) for p in prompts}
    current_user.favorited_prompts = {
        str(fav.prompt.id) for fav in Favorite.objects(user=current_user.id)
    }

    return jsonify({"prompts": [serialize_prompt(p) for p in prompts]})


@api.route("/user/favorites")
@login_required
def get_user_favorites():
    favorited_prompt_ids = [
        fav.prompt.id for fav in Favorite.objects(user=current_user.id)
    ]
    prompts = Prompt.objects(id__in=favorited_prompt_ids).order_by("-created_at")

    # 获取用户的点赞和收藏状态
    current_user.liked_prompts = {
        str(like.prompt.id) for like in Like.objects(user=current_user.id)
    }
    current_user.favorited_prompts = {str(p.id) for p in prompts}

    return jsonify({"prompts": [serialize_prompt(p) for p in prompts]})


@api.route("/user/settings", methods=["PUT"])
@login_required
def update_user_settings():
    data = request.get_json()

    # 验证邮箱是否已被使用
    if data.get("email") and data["email"] != current_user.email:
        if User.objects(email=data["email"]).first():
            return jsonify({"message": "Email already exists"}), 400

    # 更新基本信息
    if data.get("name"):
        current_user.name = data["name"]
    if data.get("email"):
        current_user.email = data["email"]

    # 更新密码
    if data.get("current_password") and data.get("new_password"):
        if not current_user.check_password(data["current_password"]):
            return jsonify({"message": "Current password is incorrect"}), 400
        current_user.set_password(data["new_password"])

    current_user.save()

    return jsonify(
        {
            "message": "Settings updated successfully",
            "user": serialize_user(current_user),
        }
    )


@api.route("/user/avatar", methods=["POST"])
@login_required
def upload_avatar():
    if "avatar" not in request.files:
        return jsonify({"message": "No avatar file provided"}), 400

    file = request.files["avatar"]
    if not file.filename:
        return jsonify({"message": "No file selected"}), 400

    # 验证文件类型
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        return jsonify({"message": "Invalid file type"}), 400

    try:
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 添加时间戳和随机字符串以确保唯一性
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}_{filename}"

        # 保存文件
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], "avatars", unique_filename
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        # 更新用户头像 URL
        current_user.avatar_url = f"/uploads/avatars/{unique_filename}"
        current_user.save()

        return jsonify(
            {
                "message": "Avatar uploaded successfully",
                "avatar_url": current_user.avatar_url,
            }
        )
    except Exception as e:
        return jsonify({"message": "Failed to upload avatar"}), 500


@api.route("/user/avatar", methods=["DELETE"])
@login_required
def remove_avatar():
    if current_user.avatar_url:
        try:
            # 删除文件
            file_path = os.path.join(
                current_app.root_path, "static", current_user.avatar_url.lstrip("/")
            )
            if os.path.exists(file_path):
                os.remove(file_path)

            # 清除头像 URL
            current_user.avatar_url = None
            current_user.save()

            return jsonify({"message": "Avatar removed successfully"})
        except Exception as e:
            return jsonify({"message": "Failed to remove avatar"}), 500

    return jsonify({"message": "No avatar to remove"}), 400


# Admin endpoints
@api.route("/admin/prompts")
@jwt_required
@admin_required
def admin_get_prompts():
    """获取所有提示词（管理员）"""
    try:
        # 获取分页参数
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        # 获取总数
        total = Prompt.objects.count()

        # 获取分页后的提示词
        prompts = (
            Prompt.objects.order_by("-created_at")
            .skip((page - 1) * per_page)
            .limit(per_page)
        )

        # 一次性获取所有点赞和收藏数据
        if current_user.is_authenticated:
            # 预先获取所有点赞和收藏数据
            likes_map = {
                str(like.prompt.id): True for like in Like.objects(user=current_user.id)
            }
            favorites_map = {
                str(fav.prompt.id): True
                for fav in Favorite.objects(user=current_user.id)
            }

            # 为每个提示词计算点赞和收藏数
            prompts_likes = {str(p.id): Like.objects(prompt=p).count() for p in prompts}
            prompts_favorites = {
                str(p.id): Favorite.objects(prompt=p).count() for p in prompts
            }

        # 序列化提示词数据
        serialized_prompts = []
        for prompt in prompts:
            prompt_data = {
                "id": str(prompt.id),
                "title": prompt.title,
                "content": prompt.content,
                "status": prompt.status,
                "author": (
                    {
                        "id": str(prompt.author.id),
                        "name": prompt.author.name,
                        "avatar_url": prompt.author.avatar_url,
                    }
                    if prompt.author
                    else None
                ),
                "language": (
                    {
                        "id": str(prompt.language.id),
                        "name": prompt.language.name,
                        "slug": prompt.language.slug,
                    }
                    if prompt.language
                    else None
                ),
                "likes_count": prompts_likes.get(str(prompt.id), 0),
                "favorites_count": prompts_favorites.get(str(prompt.id), 0),
                "created_at": prompt.created_at.isoformat(),
                "is_liked": likes_map.get(str(prompt.id), False),
                "is_favorited": favorites_map.get(str(prompt.id), False),
            }
            serialized_prompts.append(prompt_data)

        return jsonify(
            {
                "prompts": serialized_prompts,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": (total + per_page - 1) // per_page,
                    "has_next": page * per_page < total,
                    "has_prev": page > 1,
                },
            }
        )
    except Exception as e:
        print(f"Error fetching admin prompts: {str(e)}")
        return jsonify({"message": "Failed to fetch prompts"}), 500


@api.route("/admin/prompts/<prompt_id>/status", methods=["PUT"])
@jwt_required
@admin_required
def admin_update_prompt_status(prompt_id):
    """更新提示词状态（管理员）"""
    prompt = Prompt.objects(id=prompt_id).first_or_404()
    data = request.get_json()

    if "status" not in data:
        return jsonify({"message": "Missing status field"}), 400

    try:
        new_status = PromptStatus(data["status"])
    except ValueError:
        return jsonify({"message": "Invalid status"}), 400

    prompt.status = new_status
    prompt.save()

    # 创建审核记录
    if new_status in [PromptStatus.PUBLISHED, PromptStatus.REJECTED]:
        Review(
            prompt=prompt,
            reviewer=current_user.id,
            status=(
                ReviewStatus.PUBLISHED
                if new_status == PromptStatus.PUBLISHED
                else ReviewStatus.REJECTED
            ),
        ).save()

    return jsonify(
        {
            "message": "Prompt status updated successfully",
            "prompt": serialize_prompt(prompt),
        }
    )


@api.route("/admin/prompts/<prompt_id>", methods=["PUT"])
@jwt_required
@admin_required
def admin_update_prompt(prompt_id):
    """更新提示词（管理员）"""
    try:
        # 查找提示词
        prompt = Prompt.objects(id=prompt_id).first()
        if not prompt:
            return jsonify({"error": "Prompt not found"}), 404

        data = request.get_json()

        # 验证必填字段
        if not all(key in data for key in ["title", "content", "language"]):
            return jsonify({"error": "Missing required fields"}), 400

        # 验证语言
        language = Language.objects(id=data["language"]).first()
        if not language:
            return jsonify({"error": "Invalid language"}), 400

        # 更新提示词
        prompt.title = data["title"]
        prompt.content = data["content"]
        prompt.language = language
        prompt.save()

        return (
            jsonify(
                {
                    "message": "Prompt updated successfully",
                    "prompt": serialize_prompt(prompt),
                }
            ),
            200,
        )
    except Exception as e:
        current_app.logger.error(f"Error updating prompt: {str(e)}")
        return jsonify({"error": "Failed to update prompt"}), 500


@api.route("/admin/prompts/<prompt_id>", methods=["DELETE"])
@jwt_required
@admin_required
def admin_delete_prompt(prompt_id):
    """删除提示词（管理员）"""
    try:
        # 查找提示词
        prompt = Prompt.objects(id=prompt_id).first()
        if not prompt:
            return jsonify({"error": "Prompt not found"}), 404

        # 删除相关的点赞记录
        Like.objects(prompt=prompt).delete()

        # 删除相关的收藏记录
        Favorite.objects(prompt=prompt).delete()

        # 删除相关的审核记录
        Review.objects(prompt=prompt).delete()

        # 删除提示词
        prompt.delete()

        return jsonify({"message": "Prompt deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting prompt: {str(e)}")
        return jsonify({"error": "Failed to delete prompt"}), 500


@api.route("/admin/users")
@jwt_required
@admin_required
def admin_get_users():
    """获取所有用户（管理员）"""
    users = User.objects.order_by("-created_at")
    return jsonify({"users": [serialize_user(u) for u in users]})


@api.route("/admin/users/<user_id>/role", methods=["PUT"])
@jwt_required
@admin_required
def admin_update_user_role(user_id):
    """更新用户角色（管理员）"""
    user = User.objects(id=user_id).first_or_404()
    data = request.get_json()

    if "role" not in data:
        return jsonify({"message": "Missing role field"}), 400

    try:
        new_role = UserRole(data["role"])
    except ValueError:
        return jsonify({"message": "Invalid role"}), 400

    user.role = new_role
    user.save()

    return jsonify(
        {"message": "User role updated successfully", "user": serialize_user(user)}
    )


@api.route("/prompts/stats", methods=["GET"])
def get_prompts_stats():
    """获取提示词的统计信息，包括总数和每种语言的数量"""
    try:
        # 获取所有已发布的提示词总数
        total_count = Prompt.objects(status=PromptStatus.PUBLISHED).count()

        # 按语言分组统计数量
        language_stats = []
        for language in Language.objects.all():
            count = Prompt.objects(
                status=PromptStatus.PUBLISHED, language=language.id
            ).count()
            if count > 0:  # 只返回有提示词的语言
                language_stats.append(
                    {
                        "id": str(language.id),
                        "name": language.name,
                        "slug": language.slug,
                        "count": count,
                    }
                )

        # 按数量降序排序
        language_stats.sort(key=lambda x: x["count"], reverse=True)

        # 获取热门提示词数量（likes_count >= 10）
        popular_count = Prompt.objects(
            status=PromptStatus.PUBLISHED, likes_count__gte=10
        ).count()

        return jsonify(
            {
                "total_count": total_count,
                "popular_count": popular_count,
                "language_stats": language_stats,
            }
        )

    except Exception as e:
        print(f"Error getting prompts stats: {str(e)}")
        return jsonify({"message": "Failed to get prompts stats", "error": str(e)}), 500


@api.route("/prompts/<prompt_id>", methods=["PUT"])
@jwt_required
def update_prompt(prompt_id):
    """更新提示词（普通用户）"""
    try:
        # 查找提示词
        prompt = Prompt.objects(id=prompt_id).first()
        if not prompt:
            return jsonify({"error": "Prompt not found"}), 404

        # 检查权限（只能更新自己的提示词）
        if str(prompt.author.id) != str(current_user.id):
            return jsonify({"error": "Permission denied"}), 403

        data = request.get_json()

        # 验证必填字段
        if not all(key in data for key in ["title", "content", "language"]):
            return jsonify({"error": "Missing required fields"}), 400

        # 验证语言
        language = Language.objects(id=data["language"]).first()
        if not language:
            return jsonify({"error": "Invalid language"}), 400

        # 更新提示词
        prompt.title = data["title"]
        prompt.content = data["content"]
        prompt.language = language
        prompt.save()

        return (
            jsonify(
                {
                    "message": "Prompt updated successfully",
                    "prompt": serialize_prompt(prompt),
                }
            ),
            200,
        )

    except Exception as e:
        current_app.logger.error(f"Error updating prompt: {str(e)}")
        return jsonify({"error": "Failed to update prompt"}), 500
