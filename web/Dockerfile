# 基础镜像为node，用于构建vue项目
FROM node:lts-alpine as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# 设置环境变量
ENV VUE_APP_API_URL=http://localhost:8000

RUN npm run build

# 生产环境使用nginx
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

# 将自定义的nginx配置文件复制到容器中
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
