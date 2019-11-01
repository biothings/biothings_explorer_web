import tornado.web
import tornado.template
from networkx.readwrite import json_graph
import json

from biothings_explorer.registry import Registry
from biothings_explorer.connect import ConnectTwoConcepts

reg = Registry()

colors = {1: 'green', 2: 'red', 3: 'rgba(255,168,7)'}


class DisplayHandler(tornado.web.RequestHandler):
    def post(self):
        input_cls = self.get_body_argument("input_cls")
        input_id = self.get_body_argument("input_id")
        edge1 = self.get_body_argument("edge1").split(',')
        edge2 = self.get_body_argument("edge2").split(',')
        input_val = self.get_body_argument("input_val")
        output_cls = self.get_body_argument("output_cls")
        output_id = self.get_body_argument("output_id")
        output_val = self.get_body_argument("output_val")
        _input = '.'.join([input_cls, input_id, input_val])
        _output = '.'.join([output_cls, output_id, output_val])
        self.set_status(302)
        self.redirect('/explorer/display?input=' + _input + '&output=' + _output)

    def get(self):
        _input = self.get_query_argument('input')
        _output = self.get_query_argument('output')
        #_edge1 = self.get_query_argument('edge1')
        #_edge2 = self.get_query_argument('edge2')
        input_cls, input_id, input_val = _input.split('.')
        output_cls, output_id, output_val = _output.split('.')
        rest_input = {'type': input_cls,
                      'identifier': 'bts:' + input_id,
                      'values': input_val}
        # restructure output as a dict
        rest_output = {'type': output_cls,
                       'identifier': 'bts:' + output_id,
                       'values': output_val}
        ctc = ConnectTwoConcepts(rest_input, rest_output,
                                 edge1=None, edge2=None,
                                 registry=reg)
        ctc.connect()
        # if no results found, return error message
        try:
            res = json_graph.node_link_data(ctc.G)
        except AttributeError:
            self.clear()
            self.set_status(200)
            self.write("Unable to find any connections")
            self.finish()
            return
        links = res['links']
        new_links = []
        for _link in links:
            _link['from'] = _link.pop('source')
            _link['to'] = _link.pop('target')
            _link['font'] = {'align': 'middle'}
            _link['arrows'] = 'to'
            new_links.append(_link)
        res['links'] = new_links
        new_nodes = []
        for _node in res['nodes']:
            _node['label'] = _node['identifier'][4:] + ':' + str(_node['id'])
            _node['color'] = colors[_node['level']]
            if 'equivalent_ids' in _node:
                equ_ids = []
                for k, v in _node['equivalent_ids'].items():
                    if isinstance(v, list):
                        for _v in v:
                            equ_ids.append(k + ':' + str(_v))
                    else:
                        equ_ids.append(k + ":" + str(v))
                equ_ids = '<br>'.join(equ_ids)
                _node['equivalent_ids'] = equ_ids
            new_nodes.append(_node)
        res['nodes'] = new_nodes
        if res:
            self.clear()
            self.set_status(200)
            self.render("display.html", myvalue=json.dumps(res))
            return
