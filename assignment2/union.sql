SELECT COUNT(*) FROM (SELECT term  FROM frequency where (docid='10398_txt_earn' and count=1) UNION SELECT term  FROM frequency where (docid='925_txt_trade' and count=1));
