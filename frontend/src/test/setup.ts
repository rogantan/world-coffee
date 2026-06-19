import { config } from '@vue/test-utils';
import { createPinia } from 'pinia';
import { createTestingPinia } from '@pinia/testing';

config.global.plugins = [createTestingPinia({ createPinia })];
config.global.stubs = {
  ButtonBox: true,
  InputBox: true,
  Notify: true,
};