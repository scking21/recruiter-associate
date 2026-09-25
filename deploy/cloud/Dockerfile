# Published upstream revision, independently resolved from the public registry.
FROM public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-7ce757a1745de286dd180c5c5182aca31eba8a75@sha256:6e5e1a11a8c6e2ef6ecaa5e7b429e778a9a3befaf416a09922aaaa4a5b21d647
USER root
LABEL org.opencontainers.image.source="https://github.com/scking21/recruiter-associate" \
      org.opencontainers.image.description="Plow hosted recruiter evidence review with human decisions"
COPY recruiter/ /opt/recruiter/recruiter/
COPY experiments/recruiter/ /opt/recruiter/experiments/recruiter/
COPY docs/WORKFLOW.md /opt/recruiter/docs/WORKFLOW.md
COPY LICENSE /opt/recruiter/LICENSE
COPY deploy/cloud/recruiter-tool /usr/local/bin/recruiter-tool
COPY deploy/cloud/AGENTS.md /opt/plow/prompt/AGENTS.md
COPY deploy/cloud/skills/recruiter-associate/ /opt/plow/skills/recruiter-associate/
RUN mv /opt/plow/boot/config.js /opt/plow/boot/config-upstream.js
COPY deploy/cloud/config.mjs /opt/plow/boot/config.js
COPY deploy/cloud/check.mjs /opt/recruiter/cloud-check.mjs
RUN chmod 0755 /usr/local/bin/recruiter-tool
ENV AGENT_ID=recruiter-associate AGENT_RUNTIME=OpenClaw \
    AGENT_NAME="Recruiter associate" \
    AGENT_BLURB="Cited job evidence reviews for human hiring decisions, shared with authorized collaborators."
# Intentionally no model default until the operator authorizes the hosted route.
USER node
