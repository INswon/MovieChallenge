# コンテナ内の作業ディレクトリにentrypoint.sh をコピー
COPY entrypoint.sh /app/entrypoint.sh

# 実行権限設定
RUN chmod +x /app/entrypoint.sh

# コンテナ起動時、スクリプトを実行するよう指定
ENTRYPOINT ["/app/entrypoint.sh"]
