from flask.cli import with_appcontext
import click
from .models import User, Prompt, Language, Like, Favorite, Review, UserRole, PromptStatus, ReviewStatus, PromptType
from pymongo import MongoClient
from flask import current_app

def init_cli(app):
    @app.cli.command('set-admin')
    @click.argument('email')
    @with_appcontext
    def set_admin(email):
        """Set a user as admin by email"""
        user = User.objects(email=email).first()
        if not user:
            click.echo(f'User with email {email} not found')
            return
        
        user.role = 'ADMIN'
        user.save()
        click.echo(f'User {user.name} ({user.email}) is now an admin')

    @app.cli.command('list-admins')
    @with_appcontext
    def list_admins():
        """List all admin users"""
        admins = User.objects(role='ADMIN')
        if not admins:
            click.echo('No admin users found')
            return
        
        for admin in admins:
            click.echo(f'- {admin.name} ({admin.email})')

    @app.cli.command('check-user')
    @click.argument('email')
    @with_appcontext
    def check_user(email):
        """Check user role and information"""
        user = User.objects(email=email).first()
        if not user:
            click.echo(f'User with email {email} not found')
            return
        
        click.echo(f'User Information:')
        click.echo(f'- Name: {user.name}')
        click.echo(f'- Email: {user.email}')
        click.echo(f'- Role: {user.role}')
        click.echo(f'- Created at: {user.created_at}')

    @click.command('rebuild-indexes')
    @with_appcontext
    def rebuild_indexes():
        """重建数据库索引"""
        try:
            # 获取 MongoDB 连接
            client = MongoClient(current_app.config['MONGODB_SETTINGS']['host'])
            db_name = current_app.config['MONGODB_SETTINGS']['db']
            db_instance = client[db_name]

            # 删除所有集合的索引
            collections = ['prompts', 'languages', 'users', 'likes', 'favorites']
            for collection in collections:
                try:
                    print(f"正在删除 {collection} 的索引...")
                    db_instance[collection].drop_indexes()
                    print(f"成功删除 {collection} 的索引")
                except Exception as e:
                    print(f"删除 {collection} 索引时出错: {str(e)}")

            # 重新创建所有索引
            print("开始重新创建索引...")
            
            print("创建 Prompt 索引...")
            Prompt.ensure_indexes()
            
            print("创建 Language 索引...")
            Language.ensure_indexes()
            
            print("创建 User 索引...")
            User.ensure_indexes()
            
            print("创建 Like 索引...")
            Like.ensure_indexes()
            
            print("创建 Favorite 索引...")
            Favorite.ensure_indexes()

            print("所有索引重建完成！")

            # 显示所有集合的当前索引
            print("\n当前索引状态：")
            for collection in collections:
                print(f"\n{collection} 集合的索引：")
                indexes = db_instance[collection].list_indexes()
                for index in indexes:
                    print(f"  - {index['name']}: {index['key']}")

        except Exception as e:
            print(f"重建索引时发生错误: {str(e)}")
            raise click.ClickException('重建索引失败')

    @click.command('update-counts')
    @with_appcontext
    def update_counts():
        """更新所有提示的点赞和收藏计数"""
        try:
            # 首先删除索引
            print("删除现有索引...")
            # 获取 MongoDB 连接信息
            mongodb_settings = current_app.config.get('MONGODB_SETTINGS', {})
            if not mongodb_settings:
                print("无法获取 MongoDB 配置信息")
                return
            
            # 构建 MongoDB URI
            host = mongodb_settings.get('host', 'localhost')
            port = mongodb_settings.get('port', 27017)
            db_name = mongodb_settings.get('db', 'cwbeauty')
            
            if 'mongodb://' not in host:
                uri = f"mongodb://{host}:{port}"
            else:
                uri = host
            
            print(f"连接到数据库: {uri}")
            client = MongoClient(uri)
            db_instance = client[db_name]
            
            collections = ['prompts', 'languages', 'users', 'likes', 'favorites']
            for collection in collections:
                try:
                    print(f"正在删除 {collection} 的索引...")
                    db_instance[collection].drop_indexes()
                    print(f"成功删除 {collection} 的索引")
                except Exception as e:
                    print(f"删除 {collection} 索引时出错: {str(e)}")

            # 更新计数
            print("\n开始更新提示计数...")
            prompts = Prompt.objects.all()
            total = prompts.count()
            
            for i, prompt in enumerate(prompts, 1):
                old_likes = prompt.likes_count
                old_favs = prompt.favorites_count
                
                # 计算点赞和收藏数
                likes_count = Like.objects(prompt=prompt).count()
                favorites_count = Favorite.objects(prompt=prompt).count()
                
                # 更新计数
                prompt.likes_count = likes_count
                prompt.favorites_count = favorites_count
                prompt.save()
                
                print(f"更新进度: [{i}/{total}] ID: {prompt.id}")
                print(f"  点赞: {old_likes} -> {likes_count}")
                print(f"  收藏: {old_favs} -> {favorites_count}")
            
            print("\n所有提示计数更新完成！")

            # 更新语言的热度
            print("\n开始更新语言热度...")
            languages = Language.objects.all()
            for language in languages:
                # 计算该语言下已发布的提示词数量
                prompts_count = Prompt.objects(language=language, status=PromptStatus.PUBLISHED).count()
                # 计算该语言下所有提示词的总点赞数
                total_likes = sum(p.likes_count for p in Prompt.objects(language=language, status=PromptStatus.PUBLISHED))
                # 计算热度值（可以根据需要调整计算方式）
                language.popularity = prompts_count + total_likes
                language.save()
                print(f"语言 {language.name} 热度更新为: {language.popularity}")

            print("\n所有语言热度更新完成！")

            # 重新创建索引
            print("\n开始重新创建索引...")
            
            print("创建 Prompt 索引...")
            Prompt.ensure_indexes()
            
            print("创建 Language 索引...")
            Language.ensure_indexes()
            
            print("创建 User 索引...")
            User.ensure_indexes()
            
            print("创建 Like 索引...")
            Like.ensure_indexes()
            
            print("创建 Favorite 索引...")
            Favorite.ensure_indexes()

            print("所有操作完成！")
            
        except Exception as e:
            print(f"操作时发生错误: {str(e)}")
            raise click.ClickException('操作失败')

    @click.command('migrate-to-enums')
    @with_appcontext
    def migrate_to_enums():
        """将数据库中的字符串字段迁移到枚举类型"""
        click.echo('开始迁移数据库字段到枚举类型...')
        
        # 迁移用户角色
        click.echo('迁移用户角色...')
        for user in User.objects:
            try:
                # 确保角色值有效
                if user.role not in [UserRole.USER.value, UserRole.ADMIN.value]:
                    user.role = UserRole.USER.value
                user.save()
            except Exception as e:
                click.echo(f'迁移用户 {user.id} 失败: {str(e)}')
        
        # 迁移提示词状态
        click.echo('迁移提示词状态...')
        for prompt in Prompt.objects:
            try:
                # 确保状态值有效
                if prompt.status not in [s.value for s in PromptStatus]:
                    prompt.status = PromptStatus.PENDING.value
                if prompt.type not in [t.value for t in PromptType]:
                    prompt.type = PromptType.PROMPT.value
                prompt.save()
            except Exception as e:
                click.echo(f'迁移提示词 {prompt.id} 失败: {str(e)}')
        
        # 迁移审核状态
        click.echo('迁移审核状态...')
        for review in Review.objects:
            try:
                # 确保状态值有效
                if review.status not in [s.value for s in ReviewStatus]:
                    review.status = ReviewStatus.PUBLISHED.value
                review.save()
            except Exception as e:
                click.echo(f'迁移审核记录 {review.id} 失败: {str(e)}')
        
        click.echo('迁移完成！')

    app.cli.add_command(rebuild_indexes)
    app.cli.add_command(update_counts)
    app.cli.add_command(migrate_to_enums) 