{% macro listagg_grouped(database_name, target_schema, model_name, group_by) %}
    {% set columns_query %}
       select column_name
        from information_schema.columns
        where table_schema = '{{ target_schema }}'
        and table_name = '{{ model_name }}'
        and column_name != '{{ group_by }}'
    {% endset %}
    {% set result = run_query(columns_query) %}

    -- Log the raw result of the query
    {% if result is none %}
        {% do log('Error: No result returned for columns query.', info=true) %}
    {% else %}
        {% set column_names = [] %}
        {% for row in result %}
            {% set column_name = row[0] %}
            {% do column_names.append(column_name) %}
        {% endfor %}
        {% set column_names_str = column_names | join(', ') %}
    {% endif %}

    -- Building the query with dynamic column aggregation using LISTAGG
    {% set dynamic_query %}
        select
            "{{ group_by }}",
            {% for column in column_names %}
                listagg("{{ column }}", ',') as "{{ column }}"
                {% if not loop.last %}, {% endif %}
            {% endfor %}
        from {{ database_name }}.{{ target_schema }}.{{ model_name }}
        group by "{{ group_by }}"
    {% endset %}
    {% set final_query = dynamic_query %}
    {{ final_query }}
{% endmacro %}
