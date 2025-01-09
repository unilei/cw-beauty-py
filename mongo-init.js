// 创建应用数据库和用户
db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// 创建集合
db.createCollection('users');
db.createCollection('prompts');
db.createCollection('languages');

// 创建索引
db.users.createIndex({ "email": 1 }, { unique: true });
db.prompts.createIndex({ "title": "text", "content": "text" });
db.prompts.createIndex({ "created_at": -1 });
db.prompts.createIndex({ "language": 1 });

// 创建应用数据库用户
db.createUser({
  user: process.env.MONGO_USER,
  pwd: process.env.MONGO_PASSWORD,
  roles: [
    {
      role: "readWrite",
      db: process.env.MONGO_INITDB_DATABASE
    }
  ]
});

// 插入初始语言数据
db.languages.insertMany([
  // 高频语言
  { name: "TypeScript", slug: "typescript", icon: "typescript" },
  { name: "Python", slug: "python", icon: "python" },
  { name: "React", slug: "react", icon: "react" },
  { name: "Next.js", slug: "nextjs", icon: "nextjs" },
  
  // 中频语言
  { name: "PHP", slug: "php", icon: "php" },
  { name: "C#", slug: "csharp", icon: "csharp" },
  { name: "JavaScript", slug: "javascript", icon: "javascript" },
  { name: "React Native", slug: "react-native", icon: "react" },
  { name: "Tailwind CSS", slug: "tailwind", icon: "tailwind" },
  { name: "Laravel", slug: "laravel", icon: "laravel" },
  { name: "Supabase", slug: "supabase", icon: "supabase" },
  { name: "Game Development", slug: "game-dev", icon: "gamepad" },
  { name: "Expo", slug: "expo", icon: "expo" },
  
  // 低频语言和框架
  { name: "Rust", slug: "rust", icon: "rust" },
  { name: "Web Development", slug: "web-dev", icon: "web" },
  { name: "Flutter", slug: "flutter", icon: "flutter" },
  { name: "API", slug: "api", icon: "api" },
  { name: "Vue.js", slug: "vue", icon: "vue" },
  { name: "Node.js", slug: "nodejs", icon: "nodejs" },
  { name: "Java", slug: "java", icon: "java" },
  { name: "C++", slug: "cpp", icon: "cpp" },
  { name: "Go", slug: "go", icon: "go" },
  { name: "Ruby", slug: "ruby", icon: "ruby" },
  { name: "Swift", slug: "swift", icon: "swift" },
  { name: "Kotlin", slug: "kotlin", icon: "kotlin" },
  { name: "Docker", slug: "docker", icon: "docker" },
  { name: "Kubernetes", slug: "kubernetes", icon: "kubernetes" },
  { name: "AWS", slug: "aws", icon: "aws" },
  { name: "Azure", slug: "azure", icon: "azure" },
  { name: "GraphQL", slug: "graphql", icon: "graphql" },
  { name: "MongoDB", slug: "mongodb", icon: "mongodb" },
  { name: "PostgreSQL", slug: "postgresql", icon: "postgresql" },
  { name: "Redis", slug: "redis", icon: "redis" }
]);

// 插入管理员用户
db.users.insertOne({
  email: "admin@example.com",
  name: "Admin",
  password: "hashed_password", // 注意：实际使用时需要使用哈希后的密码
  role: "admin",
  created_at: new Date()
}); 