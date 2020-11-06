SELECT
    q_group.questionGroupID
	, q_group.description AS questionGroupDescription
	, q.questionID
    , q.description AS questionDescription
    , q_answer.answer AS participantAnswer
FROM tb_questions AS q -- tabela de perguntas
INNER JOIN tb_questiongroupform AS q_module -- tabela de modulo
    ON q_module.questionID = q.questionID
    AND q_module.crfFormsID = {module_id} -- placeholder para o modulo
LEFT JOIN tb_questiongroup AS q_group -- tabela de agrupamento
	ON q_group.questionGroupID = q.questionGroupID
LEFT JOIN (
	SELECT 
		form.crfFormsID
        , q_answer.questionID
        , form.participantID
        , q_answer.answer
    FROM tb_formrecord AS form -- tabela de paciente que responde a pesquisa
    INNER JOIN tb_questiongroupformrecord AS q_answer -- tabela de agrupamento
		USING (formRecordID)
	WHERE form.participantID = {participant_id} -- placeholder para participante
) AS q_answer
	ON q_answer.crfFormsID = q_module.crfFormsID
    AND q_answer.questionID = q_module.questionID
ORDER BY q_module.questionOrder;