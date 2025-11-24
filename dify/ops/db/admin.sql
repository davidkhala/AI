-- show accounts
select id, name, mode
from apps
where status = 'normal';
-- list apps
select name, email
from accounts
where status = 'active'
;

-- app config details. since this is a change history table, app_id is not unique in this table.
select app_id,
       opening_statement,
       suggested_questions,
       suggested_questions_after_answer,
       model,
       pre_prompt,
       agent_mode,
       speech_to_text,
       sensitive_word_avoidance,
       retriever_resource,
       prompt_type,
       chat_prompt_config,
       completion_prompt_config,
       dataset_configs,
       file_upload,
       text_to_speech
from app_model_configs;

select * from app_model_configs;
-- knowledge base usage
select * from dataset_queries where source = 'app' and created_by_role = 'end_user';

-- user feedback
SELECT
    mf.*,
    m.query,
    m.answer,
    m.message  -- conversation context
FROM message_feedbacks mf
LEFT JOIN messages m
    ON mf.message_id = m.id;
