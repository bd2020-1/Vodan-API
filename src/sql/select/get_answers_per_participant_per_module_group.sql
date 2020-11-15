SELECT
	q.questionID
    , q.description AS questionDescription
    , q_answer.answer AS participantAnswer
    , q_answer.description AS listParticipantAnswer
FROM tb_questions AS q
INNER JOIN tb_questiongroupform AS q_module
    ON q_module.questionID = q.questionID
    AND q_module.crfFormsID = {module_id}
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
WHERE q_group.questionGroupID = {group_id} and 
q_answer.dtRegistroForm = (SELECT MAX(dtRegistroForm) FROM tb_formrecord where participantID ={participant_id} and crfFormsID = {module_id})
ORDER BY q_module.questionOrder;