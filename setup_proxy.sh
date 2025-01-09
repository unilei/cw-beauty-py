#!/bin/bash

# 代理配置
proxy_on() {
    export http_proxy=http://127.0.0.1:7890
    export https_proxy=http://127.0.0.1:7890
    export all_proxy=socks5://127.0.0.1:7890
    
    # 设置 Git 代理
    git config --global http.proxy http://127.0.0.1:7890
    git config --global https.proxy http://127.0.0.1:7890
    
    # 设置 npm 代理
    npm config set proxy http://127.0.0.1:7890
    npm config set https-proxy http://127.0.0.1:7890
    
    echo "✅ 代理已开启"
    proxy_status
}

proxy_off() {
    unset http_proxy
    unset https_proxy
    unset all_proxy
    
    # 取消 Git 代理
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    
    # 取消 npm 代理
    npm config delete proxy
    npm config delete https-proxy
    
    echo "❌ 代理已关闭"
}

proxy_status() {
    echo "当前代理状态:"
    echo "--------------------------------"
    echo "HTTP  代理: ${http_proxy:-未设置}"
    echo "HTTPS 代理: ${https_proxy:-未设置}"
    echo "SOCKS 代理: ${all_proxy:-未设置}"
    echo "--------------------------------"
    echo "正在通过 curl 验证代理..."
    curl -s ipinfo.io
}

# 导出函数，使其可用
export -f proxy_on
export -f proxy_off
export -f proxy_status

# 创建别名
alias proxy="proxy_status"
alias pon="proxy_on"
alias poff="proxy_off"

# 显示使用说明
echo "代理命令已设置完成！"
echo "使用方法："
echo "  pon        - 开启代理"
echo "  poff       - 关闭代理"
echo "  proxy      - 查看代理状态"
