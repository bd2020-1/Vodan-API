SELECT *
FROM tb_questiongroup
WHERE questionGroupID IN (
    SELECT questionGroupID
    FROM tb_questiongroupform AS PV INNER JOIN tb_questions AS Q
    ON PV.crfFormsID = {module_id} AND PV.questionID = Q.questionID
    GROUP BY questionGroupID
)