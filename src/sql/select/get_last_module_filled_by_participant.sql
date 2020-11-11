SELECT
    form.crfFormsID
    , form.description
    , participant.dtRegistroForm
FROM project_vodan.tb_crfforms as form
INNER JOIN project_vodan.tb_formrecord as participant
    ON participant.crfFormsID = form.crfFormsID
    AND participant.participantID = {participant_id} -- placeholder received in field for participantID
ORDER BY
	participant.dtRegistroForm DESC
    , form.crfFormsID DESC
LIMIT 1