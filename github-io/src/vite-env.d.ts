/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_BASE_PATH?: string;
  readonly VITE_STARTER_PACKAGE_WHEEL_URL?: string;
  readonly VITE_CADBUILDR_SDK_KEY_ID?: string;
  readonly VITE_CADBUILDR_HUB_BASE_URL?: string;
  readonly VITE_KERNEL_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
