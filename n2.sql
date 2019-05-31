
CREATE OR REPLACE FUNCTION _final_median(NUMERIC[])
   RETURNS NUMERIC AS
$$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$$
LANGUAGE 'sql' IMMUTABLE;

CREATE AGGREGATE median(NUMERIC) (
  SFUNC=array_append,
  STYPE=NUMERIC[],
  FINALFUNC=_final_median,
  INITCOND='{}'
);


SELECT DISTINCT t1.time, t1.value, MIN(t2.value) OVER(PARTITION BY t1.time), MAX(t2.value) OVER(PARTITION BY t1.time) AS max, avg(t2.value) OVER(PARTITION BY t1.time) AS avg, median(t2.value) OVER(PARTITION BY t1.time) AS median
  FROM public.test AS t1 INNER JOIN public.test AS t2 ON t2.time > (t1.time - interval '100 seconds') AND t2.time <= t1.time ORDER BY t1.time;

SELECT DISTINCT DATE(t1.time) AS "date", MIN(t1.value) AS min, MAX(t1.value) AS max, AVG(t1.value) AS avg, median(t1.value) AS median FROM public.test AS t1 GROUP BY DATE(t1.time) ORDER BY "date" ;