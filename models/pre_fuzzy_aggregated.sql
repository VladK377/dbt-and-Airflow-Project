{{
    config(
        materialized = 'table'
    )
}}


{{ listagg_grouped('ADP_WORKSPACES','AE', 'SOURCES_FOR_FUZZY', 'Account UUID') }}



