from app import create_app
from app.models import User, Language, Prompt
from werkzeug.security import generate_password_hash
from datetime import datetime, UTC

def seed_database():
    app = create_app()
    with app.app_context():
        # 清除现有数据
        User.objects.delete()
        Language.objects.delete()
        Prompt.objects.delete()

        # 创建语言
        languages = [
            # 高频语言 (10+ mentions)
            Language(name="TypeScript", slug="typescript", icon="typescript"),
            Language(name="Python", slug="python", icon="python"),
            Language(name="React", slug="react", icon="react"),
            Language(name="Next.js", slug="nextjs", icon="nextjs"),
            
            # 中频语言 (4-9 mentions)
            Language(name="PHP", slug="php", icon="php"),
            Language(name="C#", slug="csharp", icon="csharp"),
            Language(name="JavaScript", slug="javascript", icon="javascript"),
            Language(name="React Native", slug="react-native", icon="react"),
            Language(name="Tailwind CSS", slug="tailwind", icon="tailwind"),
            Language(name="Laravel", slug="laravel", icon="laravel"),
            Language(name="Supabase", slug="supabase", icon="supabase"),
            Language(name="Game Development", slug="game-dev", icon="gamepad"),
            Language(name="Expo", slug="expo", icon="expo"),
            
            # 低频语言和框架 (2-3 mentions)
            Language(name="Rust", slug="rust", icon="rust"),
            Language(name="Web Development", slug="web-dev", icon="web"),
            Language(name="Flutter", slug="flutter", icon="flutter"),
            Language(name="API", slug="api", icon="api"),
            Language(name="Meta-Prompt", slug="meta-prompt", icon="prompt"),
            Language(name="Vite", slug="vite", icon="vite"),
            Language(name="SvelteKit", slug="sveltekit", icon="svelte"),
            Language(name="WordPress", slug="wordpress", icon="wordpress"),
            Language(name="Angular", slug="angular", icon="angular"),
            Language(name="Blockchain", slug="blockchain", icon="blockchain"),
            Language(name="Unity", slug="unity", icon="unity"),
            Language(name="FastAPI", slug="fastapi", icon="fastapi"),
            Language(name="GraphQL", slug="graphql", icon="graphql"),
            Language(name="Alpine.js", slug="alpinejs", icon="alpinejs"),
            Language(name="Accessibility", slug="a11y", icon="accessibility"),
            Language(name="Ionic", slug="ionic", icon="ionic"),
            Language(name="Cordova", slug="cordova", icon="cordova"),
            Language(name="Java", slug="java", icon="java"),
            Language(name="Zod", slug="zod", icon="zod"),
            Language(name="Zustand", slug="zustand", icon="zustand"),
            Language(name="NestJS", slug="nestjs", icon="nestjs"),
            Language(name="Node.js", slug="nodejs", icon="nodejs"),
            Language(name="Nuxt.js", slug="nuxtjs", icon="nuxtjs"),
            Language(name="Vue.js", slug="vue", icon="vue"),
            Language(name="Svelte", slug="svelte", icon="svelte"),
            Language(name="SwiftUI", slug="swiftui", icon="swift"),
            Language(name="Swift", slug="swift", icon="swift"),
            Language(name="Terraform", slug="terraform", icon="terraform"),
            Language(name="FPGA", slug="fpga", icon="fpga"),
            
            # 单次提及的技术和框架
            Language(name="AL", slug="al", icon="al"),
            Language(name="Business Central", slug="business-central", icon="business"),
            Language(name="Android", slug="android", icon="android"),
            Language(name="Kotlin", slug="kotlin", icon="kotlin"),
            Language(name="Astro", slug="astro", icon="astro"),
            Language(name="AutoHotkey", slug="autohotkey", icon="autohotkey"),
            Language(name="Blazor", slug="blazor", icon="blazor"),
            Language(name="ASP.NET Core", slug="aspnet-core", icon="dotnet"),
            Language(name="Cosmos", slug="cosmos", icon="cosmos"),
            Language(name="CosmWasm", slug="cosmwasm", icon="cosmwasm"),
            Language(name="IBC", slug="ibc", icon="ibc"),
            Language(name="Bootstrap", slug="bootstrap", icon="bootstrap"),
            Language(name="Chrome Extension", slug="chrome-ext", icon="chrome"),
            Language(name="Browser API", slug="browser-api", icon="browser"),
            Language(name="Convex", slug="convex", icon="convex"),
            Language(name="C++", slug="cpp", icon="cpp"),
            Language(name="Data Analysis", slug="data-analysis", icon="data"),
            Language(name="Jupyter", slug="jupyter", icon="jupyter"),
            Language(name="Deep Learning", slug="deep-learning", icon="dl"),
            Language(name="PyTorch", slug="pytorch", icon="pytorch"),
            Language(name="Transformer", slug="transformer", icon="transformer"),
            Language(name="LLM", slug="llm", icon="llm"),
            Language(name="Diffusion", slug="diffusion", icon="diffusion"),
            Language(name="DevOps", slug="devops", icon="devops"),
            Language(name="Kubernetes", slug="kubernetes", icon="kubernetes"),
            Language(name="Azure", slug="azure", icon="azure"),
            Language(name="Bash", slug="bash", icon="bash"),
            Language(name="Ansible", slug="ansible", icon="ansible"),
            Language(name="Django", slug="django", icon="django"),
            Language(name=".NET", slug="dotnet", icon="dotnet"),
            Language(name="Elixir", slug="elixir", icon="elixir"),
            Language(name="Phoenix", slug="phoenix", icon="phoenix"),
            Language(name="Microservices", slug="microservices", icon="microservices"),
            Language(name="Serverless", slug="serverless", icon="serverless"),
            Language(name="Fastify", slug="fastify", icon="fastify"),
            Language(name="Flask", slug="flask", icon="flask"),
            Language(name="Gatsby", slug="gatsby", icon="gatsby"),
            Language(name="Ghost", slug="ghost", icon="ghost"),
            Language(name="Go", slug="go", icon="go"),
            Language(name="HTML", slug="html", icon="html"),
            Language(name="CSS", slug="css", icon="css"),
            Language(name="HTMX", slug="htmx", icon="htmx"),
            Language(name="Firebase", slug="firebase", icon="firebase"),
            Language(name="Firestore", slug="firestore", icon="firebase"),
            Language(name="Spring", slug="spring", icon="spring"),
            Language(name="Spring Boot", slug="spring-boot", icon="spring"),
            Language(name="Quarkus", slug="quarkus", icon="quarkus"),
            Language(name="Jakarta EE", slug="jakarta-ee", icon="jakarta"),
            Language(name="MicroProfile", slug="microprofile", icon="microprofile"),
            Language(name="GraalVM", slug="graalvm", icon="graalvm"),
            Language(name="Vert.x", slug="vertx", icon="vertx"),
            Language(name="JAX", slug="jax", icon="jax"),
            Language(name="Machine Learning", slug="ml", icon="ml"),
            Language(name="Julia", slug="julia", icon="julia"),
            Language(name="Data Science", slug="data-science", icon="datascience"),
            Language(name="Livewire", slug="livewire", icon="livewire"),
            Language(name="DaisyUI", slug="daisyui", icon="daisyui"),
            Language(name="Lua", slug="lua", icon="lua"),
            Language(name="Tamagui", slug="tamagui", icon="tamagui"),
            Language(name="Monorepo", slug="monorepo", icon="monorepo"),
            Language(name="Solito", slug="solito", icon="solito"),
            Language(name="i18n", slug="i18n", icon="i18n"),
            Language(name="Stripe", slug="stripe", icon="stripe"),
            Language(name="Redux", slug="redux", icon="redux"),
            Language(name="Viem", slug="viem", icon="viem"),
            Language(name="Wagmi", slug="wagmi", icon="wagmi"),
            Language(name="Standard.js", slug="standardjs", icon="standard"),
            Language(name="Radix UI", slug="radix", icon="radix"),
            Language(name="Shadcn UI", slug="shadcn", icon="shadcn"),
            Language(name="OnchainKit", slug="onchainkit", icon="onchain"),
            Language(name="Pixi.js", slug="pixijs", icon="pixi"),
            Language(name="Testing", slug="testing", icon="testing"),
            Language(name="Ruby", slug="ruby", icon="ruby"),
            Language(name="Ruby on Rails", slug="rails", icon="rails"),
            Language(name="Three.js", slug="threejs", icon="threejs"),
            Language(name="React Three Fiber", slug="r3f", icon="r3f"),
            Language(name="Remix", slug="remix", icon="remix"),
            Language(name="RoboCorp", slug="robocorp", icon="robocorp"),
            Language(name="Salesforce", slug="salesforce", icon="salesforce"),
            Language(name="SFDX", slug="sfdx", icon="sfdx"),
            Language(name="Force.com", slug="force", icon="force"),
            Language(name="Solana", slug="solana", icon="solana"),
            Language(name="Anchor", slug="anchor", icon="anchor"),
            Language(name="Web3.js", slug="web3", icon="web3"),
            Language(name="Metaplex", slug="metaplex", icon="metaplex"),
            Language(name="Solidity", slug="solidity", icon="solidity"),
            Language(name="Smart Contracts", slug="smart-contracts", icon="smartcontract"),
            Language(name="Ethereum", slug="ethereum", icon="ethereum"),
            Language(name="Paraglide.js", slug="paraglidejs", icon="paraglide"),
            Language(name="Tauri", slug="tauri", icon="tauri"),
            Language(name="Technical Writing", slug="tech-writing", icon="writing"),
            Language(name="UI/UX Design", slug="uiux", icon="design"),
            Language(name="SystemVerilog", slug="systemverilog", icon="sv"),
            Language(name="Docker", slug="docker", icon="docker"),
            Language(name="Web Scraping", slug="web-scraping", icon="scraping"),
            Language(name="Jina AI", slug="jina", icon="jina"),
            Language(name="WooCommerce", slug="woocommerce", icon="woo")
        ]
        for lang in languages:
            lang.save()

        # 创建管理员用户
        admin = User(
            email="admin@example.com",
            name="Admin",
            password=generate_password_hash("admin123"),
            role="admin",
            created_at=datetime.now(UTC)
        )
        admin.save()

        # 创建示例提示词
        python_lang = Language.objects(slug="python").first()
        example_prompt = Prompt(
            title="Python FastAPI Example",
            content="Create a FastAPI application with user authentication",
            language=python_lang,
            author=admin,
            created_at=datetime.now(UTC)
        )
        example_prompt.save()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database() 