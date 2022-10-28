## 유튜브의 강의를 재생목록 url로 파싱하는 스크립트 (미완)
 
- v0.0.1
  
### TO-DO
- [ ] directory 나누기
- [ ] 터미널에서 실행 시 재생 목록 id argument 입력할 수 있도록
- [ ] Type 적용 수정하기
- [ ] 저장 기능 수정하기



### 참고한 글들
time diff   
https://stackoverflow.com/questions/61568859/difference-between-two-dates-datetime



### Errors
- 'types.GenericAlias' object is not iterable
  - https://stackoverflow.com/questions/64938827/type-error-types-genericalias-object-is-not-iterable
```py
# 이게 아니고
def make_pl_list() -> list(dict[str, Any]):
# 이렇게 해야
def make_pl_list() -> list[dict[str, Any]]:
```

- vars() argument must have __dict__ attribute