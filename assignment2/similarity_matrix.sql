select sum( A.count * B.count )
from frequency A, frequency B
where A.term = B.term  and A.docid < B.docid 
group by A.docid, B.docid;

