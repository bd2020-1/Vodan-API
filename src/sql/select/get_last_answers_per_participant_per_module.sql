SELECT
	q.questionID
    , q.description AS questionDescription
    , q_answer.answer AS participantAnswer
    , q_answer.description AS listParticipantAnswer
    , q_module.crfFormsID
    , (SELECT description FROM tb_crfforms WHERE crfFormsID = q_module.crfFormsID) AS formName
FROM tb_questions AS q
INNER JOIN tb_questiongroupform AS q_module
    ON q_module.questionID = q.questionID
    AND q_module.crfFormsID = (SELECT MAX(crfFormsID) FROM tb_formrecord where participantID = {participant_id})
LEFT JOIN tb_questiongroup AS q_group
	ON q_group.questionGroupID = q.questionGroupID
LEFT JOIN (
	SELECT
		form.crfFormsID
        , q_answer.questionID
        , form.participantID
        , q_answer.answer
        , q_answer.listOfValuesID
        , list_answer.description
        ,form.dtRegistroForm
    FROM tb_questiongroupformrecord AS q_answer
    INNER JOIN tb_formrecord AS form
		ON form.formRecordID = q_answer.formRecordID
        AND form.participantID = {participant_id}
	LEFT JOIN tb_listofvalues AS list_answer
		ON q_answer.listOfValuesID = list_answer.listOfValuesID
) AS q_answer
	ON q_answer.crfFormsID = q_module.crfFormsID
    AND q_answer.questionID = q_module.questionID
where q_answer.dtRegistroForm = (SELECT MAX(dtRegistroForm) FROM tb_formrecord where participantID = {participant_id})
ORDER BY q_module.questionOrder;