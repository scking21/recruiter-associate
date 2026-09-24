FROM node:24.16.0-bookworm-slim
LABEL org.opencontainers.image.source="https://github.com/scking21/recruiter-associate" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.description="Recruiter evidence review with human hiring decisions"

RUN apt-get update && apt-get install -y --no-install-recommends python3 ca-certificates git \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g openclaw@2026.9.5 \
    && npm cache clean --force
WORKDIR /app
COPY --chown=node:node recruiter/ recruiter/
COPY --chown=node:node experiments/ experiments/
COPY --chown=node:node skills/ skills/
COPY --chown=node:node scripts/ scripts/
COPY --chown=node:node deploy/ deploy/
COPY --chown=node:node docs/WORKFLOW.md docs/WORKFLOW.md
COPY --chown=node:node vendor/agent-index-client/ vendor/agent-index-client/
COPY --chown=node:node LICENSE LICENSE
RUN mkdir /data && chown node:node /data
USER node
ENV RECRUITER_STATE_ROOT=/data/recruiter OPENCLAW_STATE_DIR=/data/recruiter
EXPOSE 20789
HEALTHCHECK --interval=60s --timeout=20s --start-period=60s --retries=3 \
    CMD ["python3", "scripts/container_entrypoint.py", "health"]
ENTRYPOINT ["python3", "scripts/container_entrypoint.py"]
