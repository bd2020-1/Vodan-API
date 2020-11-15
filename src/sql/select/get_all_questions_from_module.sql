SELECT crfFormsID, PV.questionID, questionOrder, description, questionTypeID, listTypeID, questionGroupID, subordinateTo, isAbout
FROM tb_questiongroupform AS PV INNER JOIN tb_questions AS Q
ON PV.crfFormsID = {module_id} AND PV.questionID = Q.questionID
ORDER BY questionOrder;