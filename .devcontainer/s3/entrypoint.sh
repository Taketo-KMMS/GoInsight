#!/bin/sh

# 権限を作成
mkdir -p /data/.minio.sys/buckets
cp -r /policies/* /data/.minio.sys/

# 権限が与えられたバケットを作成
rsync -avz --include='*/' --exclude='*' /policies/buckets/ /data/

# サーバー起動
minio server /data --address :9000 --console-address ':9001'
