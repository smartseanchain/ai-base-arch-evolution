# 静态站点：使用 busybox httpd（镜像小，易拉取成功）
FROM busybox:1.36
WORKDIR /www
COPY . /www
EXPOSE 80
# -f 前台 -p 端口 -h 站点根目录
CMD ["httpd", "-f", "-p", "80", "-h", "/www"]
