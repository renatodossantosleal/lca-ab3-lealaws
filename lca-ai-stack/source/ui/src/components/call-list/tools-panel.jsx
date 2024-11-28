// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
import React from 'react';
import HelpPanel from '@cloudscape-design/components/help-panel';

const header = <h2>Calls</h2>;
const content = (
  <>
    <p>Veja uma lista de chamadas e informações relacionadas</p>
    <p>Use a barra de pesquisa para filtrar por qualquer campo.</p>
    <p>Para mais detalhes selecione uma chamada específica</p>
  </>
);

const ToolsPanel = () => <HelpPanel header={header}>{content}</HelpPanel>;

export default ToolsPanel;
