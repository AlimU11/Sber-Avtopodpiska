--- query to select raw data

WITH session_target
AS (SELECT
    h.session_id,
    MAX(CASE WHEN h.event_action IN ('sub_car_claim_click',
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
    FROM {0} h
    GROUP BY h.session_id)

SELECT
    CASE
        WHEN s.utm_source IN ('QxAxdyPLuQMEcrdZWdWb',
                             'MvfHsxITijuriZxsqZqt',
                             'ISrKoXQCxqqYvAZICvjs',
                             'IZEXUFLARCUMynmHNBGo',
                             'PlbkrSYoHuZBWfYjYnfw',
                             'gVRrcxiDQubJiljoTbGm')
                            THEN true
        ELSE false
    END as utm_source,
    CASE
        WHEN s.utm_medium IN ('organic', 'referral', '(none)') THEN true
        ELSE false
    END as utm_medium,
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
FROM {1} s
INNER JOIN session_target t
    ON s.session_id = t.session_id
;
