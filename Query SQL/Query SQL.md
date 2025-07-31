# Query para comparar as vendas de hoje com a média da semana anterior, por hora.

## O objetivo é visualizar a queda abrupta que indica a anomalia.
```
SELECT
    time,
    today,
    avg_last_week
FROM
    checkouts -- (Imaginando que os dados estão em uma tabela chamada 'checkouts')
ORDER BY
    CAST(REPLACE(time, 'h', '') AS INTEGER);
```

