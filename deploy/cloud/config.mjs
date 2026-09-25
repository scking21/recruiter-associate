import { renderConfig as upstreamConfig } from './config-upstream.js';

// Only this variant changes model selection; native installs remain on NVIDIA.
export function renderConfig(identity, apiBase) {
  const config = upstreamConfig(identity, apiBase);
  const model = process.env.RECRUITER_CLOUD_MODEL;
  if (model !== 'z-ai/glm-5.2') {
    throw new Error('Hosted model approval required: RECRUITER_CLOUD_MODEL must explicitly name z-ai/glm-5.2');
  }
  const provider = config.models.providers.plow;
  const selected = provider.models.find(entry => entry.id === model);
  if (!selected) throw new Error('Pinned Plow base does not support the selected model');
  provider.models = [selected];
  config.agents.defaults.model = { primary: `plow/${model}`, fallbacks: [] };
  // Replies in the incoming conversation use the channel adapter, not these tools.
  config.tools.alsoAllow = config.tools.alsoAllow.filter(tool => tool !== 'plow_start_thread');
  config.tools.deny = [...config.tools.deny, 'message', 'plow_start_thread'];
  return config;
}
