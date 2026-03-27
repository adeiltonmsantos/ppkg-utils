{% csrf_token %}
<div class="fields-container">
{% for field in form %}
    <div class="form-field">
        {{ field.label_tag }}
        {{ field }}
        {% if field.name == 'img_uf' and path_brasao != 'None' %}
            <img class="img_ipem_data" src="{{ MEDIA_URL }}brasao.png" alt="Imagem do brasão do estado do IPEM">
        {% endif %}
        {% if field.name == 'img_conv' and path_convenio != 'None' %}
            <img class="img_ipem_data" src="{{ MEDIA_URL }}convenio.png" alt="Imagem do convênio INMETRO/IPEM">
        {% endif %}

        {% if field.errors %}
            <div class="error-messages">
                {{ field.errors }}
            </div>
        {% endif %}
    </div>
{% endfor %}
</div>
