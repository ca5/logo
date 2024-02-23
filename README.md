
# Ca5 logo generator
## deploy
python3.12とgcloudの相性が悪いので、pyenv環境でやる場合は外のdirからコマンド実行をする
```
gcloud functions deploy logo \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--source=./logo/ \
--entry-point=main \
--trigger-http
```