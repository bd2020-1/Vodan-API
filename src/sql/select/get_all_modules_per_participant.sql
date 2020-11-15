SELECT formRecordID, CAST(dtRegistroForm as DATE) as dtRegisterForm , c.crfFormsID, a.description as FormsName FROM tb_formrecord c
LEFT join tb_assessmentquestionnaire b 
ON b.participantID = c.participantID
LEFT join tb_crfforms a
on c.crfFormsID = a.crfFormsID
where b.participantID ={participant_id}
and c.crfFormsID IN {tuple_modules}
order by crfFormsID, dtRegistroForm;