SELECT formRecordID, CAST(dtRegistroForm as DATE) as dtRegistroForm , crfFormsID FROM tb_formrecord c
LEFT join tb_assessmentquestionnaire b 
ON b.participantID = c.participantID
where b.participantID ={participant_id}
order by crfFormsID, dtRegistroForm;