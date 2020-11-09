SELECT
	q.questionID
    , q.description AS questionDescription
    , q_answer.answer AS participantAnswer
FROM tb_questions AS q -- tabela de perguntas
INNER JOIN tb_questiongroupform AS q_module -- tabela de modulo
    ON q_module.questionID = q.questionID
    AND q_module.crfFormsID = {module_id} -- placeholder para o modulo
LEFT JOIN tb_questiongroup AS q_group -- tabela de agrupamento das perguntas
	ON q_group.questionGroupID = q.questionGroupID
LEFT JOIN (
	SELECT
		form.crfFormsID
        , q_answer.questionID
        , form.participantID
        , q_answer.answer
    FROM tb_formrecord AS form  -- tabela de cadastro de formulario respondida pelo paciente
    INNER JOIN tb_questiongroupformrecord AS q_answer -- tabela de respostas com as pesquisas do formulario
		USING (formRecordID)
	WHERE form.participantID = {participant_id} -- placeholder para participante
) AS q_answer
	ON q_answer.crfFormsID = q_module.crfFormsID
    AND q_answer.questionID = q_module.questionID
WHERE q_group.questionGroupID = {group_id}
ORDER BY q_module.questionOrder;