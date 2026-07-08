{{- define "cavra.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "cavra.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "cavra.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
app.kubernetes.io/name: {{ include "cavra.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "cavra.selectorLabels" -}}
app.kubernetes.io/name: {{ include "cavra.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "cavra.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "cavra.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}

{{- define "cavra.postgresqlHost" -}}
{{- if .Values.postgresql.enabled -}}
{{- printf "%s-postgresql" .Release.Name -}}
{{- else -}}
{{- .Values.externalPostgresql.host -}}
{{- end -}}
{{- end -}}

{{- define "cavra.postgresqlDsn" -}}
{{- $host := include "cavra.postgresqlHost" . -}}
{{- $port := .Values.externalPostgresql.port | default 5432 -}}
{{- $db := .Values.externalPostgresql.database | default .Values.postgresql.auth.database -}}
{{- $user := .Values.externalPostgresql.username | default .Values.postgresql.auth.username -}}
{{- $sslmode := .Values.externalPostgresql.sslmode | default "require" -}}
{{- printf "postgresql://%s:$(CAVRA_POSTGRES_PASSWORD)@%s:%v/%s?sslmode=%s" $user $host $port $db $sslmode -}}
{{- end -}}
