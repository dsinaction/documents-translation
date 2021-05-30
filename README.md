# Documents-Translation

Prosty system umożliwiający automatycznie tłumaczenie dokumentów wykorzystujący komponenty w ramach Google Cloud Platorm. System został oparty na Cloud Functions, Cloud Translation oraz Cloud Storage.

1. Tworzymy buckety, w których przechowywane będą dokumenty źródłowe oraz dokumenty przełumaczone.

```bash
export BUCKET_TO_TRANSLATE=dsinaction-translate
export BUCKET_TRANSLATED=dsinaction-translated
```

```bash
gsutil mb gs://$BUCKET_TO_TRANSLATE
gsutil mb gs://$BUCKET_TRANSLATED
```

2. Wgrywamy skyprt na środowisko uruchomieniowe.

```bash
gcloud functions deploy translate_gcs \
--runtime python38 \
--entry-point=main \
--set-env-vars BUCKET_TRANSLATED=$BUCKET_TRANSLATED \
--trigger-resource gs://$BUCKET_TO_TRANSLATE \
--trigger-event google.storage.object.finalize
```

3. Wgrywamy przykładowe dokumenty.

```bash
gsutil cp documents/russian_women.txt gs://$BUCKET_TO_TRANSLATE
gsutil cp documents/grasshopper.txt gs://$BUCKET_TRANSLATED
```

4. Po chwili w naszym drugim buckecie powinny pojawić się przetłumaczone pliki.

```bash
gsutil ls gs://$BUCKET_TRANSLATED
gsutil cat gs://$BUCKET_TRANSLATED/russian_women.txt
```

5. Kiedy zakończymy testowanie naszego rozwiązania, możemy usunąć funkcję oraz dane:

```bash
gcloud functions delete translate-documents
gsutil rm -r gs://$BUCKET_TO_TRANSLATE
gsutil rm -r gs://$BUCKET_TRANSLATED
```