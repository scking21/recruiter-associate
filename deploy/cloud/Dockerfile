# Published upstream revision, independently resolved from the public registry.
ARG PLOW_BASE=public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-7ce757a1745de286dd180c5c5182aca31eba8a75@sha256:6e5e1a11a8c6e2ef6ecaa5e7b429e778a9a3befaf416a09922aaaa4a5b21d647
FROM ${PLOW_BASE}
USER root
LABEL org.opencontainers.image.source="https://github.com/scking21/recruiter-associate" \
      org.opencontainers.image.description="Plow hosted Roletrace evidence review with human decisions"
COPY recruiter/ /opt/recruiter/recruiter/
COPY experiments/recruiter/ /opt/recruiter/experiments/recruiter/
COPY docs/WORKFLOW.md /opt/recruiter/docs/WORKFLOW.md
COPY LICENSE /opt/recruiter/LICENSE
COPY deploy/cloud/recruiter-tool /usr/local/bin/recruiter-tool
COPY deploy/cloud/AGENTS.md /opt/plow/prompt/AGENTS.md
COPY deploy/cloud/skills/recruiter-associate/ /opt/plow/skills/recruiter-associate/
# A verified Roletrace parent already preserves upstream. Never wrap our wrapper.
RUN if [ -e /opt/plow/boot/config-upstream.js ]; then \
      test -f /opt/plow/boot/config-upstream.js; \
    else mv /opt/plow/boot/config.js /opt/plow/boot/config-upstream.js; fi
COPY deploy/cloud/config.mjs /opt/plow/boot/config.js
COPY deploy/cloud/check.mjs /opt/recruiter/cloud-check.mjs
RUN chmod 0755 /usr/local/bin/recruiter-tool
ENV AGENT_ID=recruiter-associate AGENT_RUNTIME=OpenClaw \
    AGENT_NAME="Roletrace" \
    AGENT_BLURB="Turn hiring evidence into a cited review. See what changes when a teammate corrects a source, keep the previous version, and leave hiring decisions with the owner."
# Approved September 25 for this hosted variant only; config removes fallbacks.
ENV RECRUITER_CLOUD_MODEL=z-ai/glm-5.2
USER node
