# PY-BLOCKCHAIN-VOTES

### Todo:
- подсчёт голосов
- окна просмотра блоков не в отдельной вкладке
- фикс API
- фикс баги
- завезти фиксированные значения входных данных - где нужна строка - только строка, где нужен int - только int

### Settings:
- все данные храниятся в памяти (:memory: в модуле sqlite3), после перезагрузки проекта все данные слетают, нужно добавить или выгрузку/загрузку, или хранить в локальном файле (вместо :memory: указать название к примеру - "blocks.db")