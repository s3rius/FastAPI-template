echo "Your deploy steps must run here"

{% if cookiecutter.add_systemd == "True" -%}
# Function to replace stub values in service files
function replace_stubs() {
  sed -i "s#WorkingDirectory=.*#WorkingDirectory=${APP_DIR:?}#" "$1"
  sed -i "s#EnvironmentFile=ENV_FILE*#EnvironmentFile=${ENV_FILE_PATH:?}#" "$1"
}

replace_stubs "./systemd/{{ cookiecutter.project_name }}_service.service"
{% if cookiecutter.add_scheduler == "True" -%}
replace_stubs "./systemd/{{ cookiecutter.project_name }}_scheduler.service"
{% endif %}
{% endif %}