// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
import React from 'react';
import { Route, Switch } from 'react-router-dom';
import SideNavigation from '@cloudscape-design/components/side-navigation';

import { CALLS_PATH, DEFAULT_PATH, STREAM_AUDIO_PATH } from '../../routes/constants';

export const callsNavHeader = { text: 'Call Analytics', href: `#${DEFAULT_PATH}` };
export const callsNavItems = [
  { type: 'link', text: 'Chamadas', href: `#${CALLS_PATH}` },
  { type: 'link', text: 'Stream de Áudio', href: `#${STREAM_AUDIO_PATH}` },
];

const defaultOnFollowHandler = () => {
  // XXX keep the locked href for our demo pages
  // ev.preventDefault();
  // console.log(ev);
};

/* eslint-disable react/prop-types */
const Navigation = ({
  activeHref = `#${STREAM_AUDIO_PATH}`,
  header = callsNavHeader,
  items = callsNavItems,
  onFollowHandler = defaultOnFollowHandler,
}) => (
  <Switch>
    <Route path={STREAM_AUDIO_PATH}>
      <SideNavigation
        items={items || callsNavItems}
        header={header || callsNavHeader}
        activeHref={activeHref || `#${STREAM_AUDIO_PATH}`}
        onFollow={onFollowHandler}
      />
    </Route>
  </Switch>
);

export default Navigation;
