--- query to select row data

WITH session_target
AS (SELECT
    h.session_id,
    MAX(CASE
        WHEN h.event_action IN ('sub_car_claim_click',
                                'sub_car_claim_submit_click',
                                'sub_open_dialog_click',
                                'sub_custom_question_submit_click',
                                'sub_call_number_click',
                                'sub_callback_submit_click',
                                'sub_submit_success',
                                'sub_car_request_submit_click')
                            THEN 1
        ELSE 0
        END) AS target_action
FROM sber_avtopodpiska.raw_hits h
GROUP BY h.session_id)

SELECT
    s.session_id,
    s.visit_date,
    s.visit_time,
    s.visit_number,
    s.utm_source,
    s.utm_medium,
    s.utm_campaign,
    s.utm_adcontent,
    s.utm_keyword,
    s.device_category,
    s.device_os,
    s.device_brand,
    s.device_model,
    s.device_screen_resolution,
    s.device_browser,
    s.geo_country,
    s.geo_city,
    t.target_action
FROM sber_avtopodpiska.raw_sessions s
INNER JOIN session_target t
    ON s.session_id = t.session_id
;
