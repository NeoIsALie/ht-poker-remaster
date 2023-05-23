1. Загрузить https://github.com/HenryRLee/PokerHandEvaluator
2. Перейти в PokerHandEvaluator/cpp
3. Добавить в makefile CFLAGS -fPIC
4. Выполнить make libphevalomaha.a
5. Скопировать libphevalomaha.a в ht-poker-remaster/fastc
6. Выполнить gcc -fPIC -shared -o evaluator.so evaluator.c libphevalomaha.a
