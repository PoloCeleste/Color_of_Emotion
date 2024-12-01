cuda 12.1 or 11.8 설치

```bash
https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_531.14_windows.exe

https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_522.06_windows.exe

https://developer.download.nvidia.com/compute/cudnn/9.5.1/local_installers/cudnn_9.5.1_windows.exe
```

pytorch 설치

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### DB 제작

1. py manage.py makemigrations
2. py manage.py migrate
3. py manage.py load_data (manage.py와 같은 경로상에 movies/management/commands 내의 json파일들 옮겨놓고 실행)
4. dumpdata
   - py -Xutf8 manage.py dumpdata movies.movie > movies/fixtures/movies/movies.json
   - py -Xutf8 manage.py dumpdata movies.genre > movies/fixtures/movies/genres.json
   - py -Xutf8 manage.py dumpdata movies.provider > movies/fixtures/movies/providers.json
   - py -Xutf8 manage.py dumpdata movies.emotion > movies/fixtures/movies/emotions.json
   - py -Xutf8 manage.py dumpdata movies.emotioncolor > movies/fixtures/movies/emotioncolors.json

#### DB 로드

- py manage.py migrate
- py manage.py loaddata movies/movies.json movies/genres.json movies/providers.json movies/emotions.json movies/emotioncolors.json

#### 모델 ERD 생성

1. pip install graphviz django-extensions pyparsing pydot

   - dot 명령어 안먹히면 [공식홈페이지](https://graphviz.org/download/)에서 설치 후 환경변수 설정해주기

   - 시스템 환경 변수에 추가

     ```md
     C:/<graphviz 설치 경로>/bin/
     C:/<graphviz 설치 경로>/bin/dot.exe
     ```

   - settings.py

     ```py
     import os
     os.environ["PATH"] += os.pathsep + 'C:/<graphviz 설치 경로>/bin/'
     ```

2. settings.py 수정

   ```py
   INSTALLED_APPS = [
      ...
      'django_extensions',
      ...
   ]

   GRAPH_MODELS = {
      'all_applications': True,
      'graph_models': True,
   }
   ```

3. ERD dot 파일 생성

   ```bash
   python manage.py graph_models -a -g -e -I Movie,Genre,Provider,Emotion,EmotionColor --arrow-shape normal --rankdir LR --dot -o movie_erd.dot
   ```

4. dot 파일 변환
   - `dot -Tpng movie_erd.dot -o movie_erd.png`
   - `dot -Tpng movie_erd.dot -o movie_erd.svg`
