select count(*) from (select docid from frequency where term='transactions' and docid in ( select docid from frequency where term='world'));
