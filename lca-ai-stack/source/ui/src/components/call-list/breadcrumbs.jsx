// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
import React from 'react';

import BreadcrumbGroup from '@cloudscape-design/components/breadcrumb-group';

import { CALLS_PATH, DEFAULT_PATH } from '../../routes/constants';

export const callListBreadcrumbItems = [
  { text: 'Analytics', href: `#${DEFAULT_PATH}` },
  { text: 'Chamadas', href: `#${CALLS_PATH}` },
];

const Breadcrumbs = () => (
  <BreadcrumbGroup ariaLabel="Breadcrumbs" items={callListBreadcrumbItems} />
);

export default Breadcrumbs;
