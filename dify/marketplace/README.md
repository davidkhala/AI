[Dify marketplace](https://marketplace.dify.ai/)
- a dev tool landscape
- [official releases](https://marketplace.dify.ai/?q=langgenius)
- [catalog:studio](../app/marketplace.md)



# Troubleshoot
`PluginDaemonBadRequestError: plugin verification has been enabled, and the plugin you want to install has a bad signature`
- configure `FORCE_VERIFYING_SIGNATURE=false` in `.env` and then restart
  - don't just `docker compose restart`. You need to split into `down` and `up`