-- Query com os emails abertos para o SAC
select distinct
    s.description as sac_subject,
    cats.description as sac_category,
    cv.description as sac_customer_voice,
    r.description as sac_reason,
    e.created_date,
    e.subject as email_subject,
    case
        when regexp_instr(eb.content, 'PROBLEMA:') is true
        and (
            regexp_instr(eb.content, 'PROBLEMA:', 1, 1, 0, 'c') - regexp_instr(eb.content, 'MENSAGEM', 1, 1, 1, 'c')
        ) > 0 then substring(
            eb.content,
            regexp_instr(eb.content, 'MENSAGEM', 1, 1, 1, 'c'),
            regexp_instr(eb.content, 'PROBLEMA:', 1, 1, 0, 'c') - regexp_instr(eb.content, 'MENSAGEM', 1, 1, 1, 'c')
        )
        when regexp_instr(eb.content, 'PROBLEMA:') is false
        and regexp_instr(eb.content, 'DETALHE:') is true then substring(
            eb.content,
            regexp_instr(eb.content, 'MENSAGEM', 1, 1, 1, 'c'),
            regexp_instr(eb.content, 'DETALHE:', 1, 1, 0, 'c') - regexp_instr(eb.content, 'MENSAGEM', 1, 1, 1, 'c')
        )
        when regexp_instr(eb.content, 'PROBLEMA:') is false
        and regexp_instr(eb.content, 'DETALHE:') is false then substring(
            eb.content,
            regexp_instr(eb.content, 'MENSAGEM', 1, 1, 1, 'c')
        )
    end as message,
    case
        when regexp_instr(eb.content, 'PROBLEMA: ') is true
        and (
            regexp_instr(eb.content, 'DETALHE:', 1, 1, 0, 'c') - regexp_instr(eb.content, 'PROBLEMA: ', 1, 1, 1, 'c')
        ) > 0 then substring(
            eb.content,
            regexp_instr(eb.content, 'PROBLEMA: ', 1, 1, 1, 'c'),
            regexp_instr(eb.content, 'DETALHE:', 1, 1, 0, 'c') - regexp_instr(eb.content, 'PROBLEMA: ', 1, 1, 1, 'c')
        )
    end as problem,
    case
        when regexp_instr(eb.content, 'DETALHE: ') is true then nullif(
            split_part(
                substring(
                    eb.content,
                    regexp_instr(eb.content, 'DETALHE: ', 1, 1, 1, 'c')
                ),
                'PROBLEMA:',
                1
            ),
            ''
        )
    end as detail,
    -- e.customer_document,
    -- e.customer_name,
    -- e.order_number,
    regexp_substr(e.email_from, '\<(.*)\>', 0, 1, 'e') as customer_email
from
    raw_king_br.protocols as p
    inner join (
        select
            p1.id_contact,
            min(p1.created_date) as min_created_date
        from
            raw_king_br.protocols as p1
        group by
            1
    ) as p2 on p.created_date = p2.min_created_date
        and p.id_contact = p2.id_contact
    inner join raw_king_br.contacts c on c.id = p.id_contact
    inner join raw_king_br.classification_matrices cm on cm.id = p.id_classification
    inner join raw_king_br.subjects s on s.id = cm.id_subject
    inner join raw_king_br.categories cats on cats.id = cm.id_category
    inner join raw_king_br.customer_voices cv on cv.id = cm.id_customer_voice
    left join raw_king_br.reasons r on r.id = cm.id_reason
    inner join raw_king_br.queue_email qe on qe.id_contact = c.id
    inner join raw_king_br.emails e on e.id = qe.id_email
    inner join raw_king_br.email_bodys eb on eb.id_email = e.id
where
    1
    and p.partition_field >= 202109
    and eb.content like 'NOME%'