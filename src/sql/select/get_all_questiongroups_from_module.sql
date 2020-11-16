SELECT q.questionGroupID, q.description, q.comment
FROM tb_questiongroup AS q
INNER JOIN (
	SELECT questionGroupID, questionOrder
	FROM tb_questiongroupform AS PV
	INNER JOIN tb_questions AS Q
		ON PV.questionID = Q.questionID
		AND PV.crfFormsID = {module_id}
) AS form
	ON q.questionGroupID = form.questionGroupID
GROUP BY q.questionGroupID, q.description, q.comment
ORDER BY MIN(form.questionOrder)