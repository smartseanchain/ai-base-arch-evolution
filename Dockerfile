# 根目录 MPA 静态站点（与 CI validate 默认真源一致）；busybox httpd，镜像小。全站 SPA 见 Dockerfile.spa · spa/README · make spa-build。
FROM busybox:1.36
WORKDIR /www
LABEL org.opencontainers.image.title="ai-base-arch-evolution-mp" \
      org.opencontainers.image.description="Static MPA (root HTML + assets + docs) via busybox httpd"
COPY . /www
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1
# -f 前台 -p 端口 -h 站点根目录
CMD ["httpd", "-f", "-p", "80", "-h", "/www"]
