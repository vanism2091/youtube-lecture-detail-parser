## 유튜브의 강의를 재생목록 url로 파싱하는 스크립트 (미완)
- v.0.0.2
- input: 재생목록 id
- output: 재생목록 내 비디오들에 대한 ["idx", "title", "url", "duration"] 정보를 담은 csv 파일

### 왜 만들었나?
이 재생 목록의 전체 강의를 다 들으려면 몇 시간이 걸릴까?
일일이 복붙/입력해서 계산하기 귀찮으니 자동화해보자.

### TO-DO
- [x] directory 나누기
- [x] Type 적용 수정하기
- [ ] 터미널에서 실행 시 재생 목록 id argument 입력할 수 있도록
- [ ] 저장 기능 수정하기
  - [ ] playlist의 video들이 저장이 안된다.. :(
- [ ] pageToken 처리하기
- [ ] 결과 csv에 재생목록 이름 추가:
  - [ ] api 추가해야 - playlist api 써야함

결과 csv는 google spreadsheet에서 불러오기
-> 얘도 스크립트로?


### 사용한 Youtube Data API
- PlaylistItems
- Videos


### 참고한 글들
Youtube API Docs
- https://developers.google.com/youtube/v3/docs/playlistItems/list


time diff   
https://stackoverflow.com/questions/61568859/difference-between-two-dates-datetime

https://www.geeksforgeeks.org/serialize-and-deserialize-complex-json-in-python/


### Errors
- 'types.GenericAlias' object is not iterable
  - https://stackoverflow.com/questions/64938827/type-error-types-genericalias-object-is-not-iterable
```py
# 이게 아니고
def make_pl_list() -> list(dict[str, Any]):
# 이렇게 해야
def make_pl_list() -> list[dict[str, Any]]:
```

TypeError: Object of type PlaylistItem is not JSON serializable
- vars() argument must have __dict__ attribute