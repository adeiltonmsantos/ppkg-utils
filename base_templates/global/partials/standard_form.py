{% csrf_token %}
<div class="fields-container">
{% for field in form %}
    <div class="form-field-collumn">
        {{ field.label_tag }}
        <div class="{% if field.widget_type == 'file' %}form-field-row{% endif %}">
            {{ field }}
                {% if field.name == 'img_uf' and path_brasao != 'None' %}
                    <img class="img_ipem_data" src="{{ MEDIA_URL }}brasao.png" alt="Imagem do brasão do estado do IPEM">
                {% endif %}
                {% if field.name == 'img_conv' and path_convenio != 'None' %}
                    <img class="img_ipem_data" src="{{ MEDIA_URL }}convenio.png" alt="Imagem do convênio INMETRO/IPEM">
                {% endif %}
        </div>
            {% if field.errors %}
            <div class="error-message-form">
                {{ field.errors }}
            </div>
        {% endif %}
    </div>
{% endfor %}
</div>
