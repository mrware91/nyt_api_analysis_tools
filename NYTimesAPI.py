import os
import time
import json
import pickle
CodeDir="/home/mrware/Dropbox/Code/NYTimes API"
JSONDir="/home/mrware/Dropbox/Code/NYTimes API/JSON"

# We will use the definitions below to save the workspace stored in memorize
WorkspaceObjects=[]

def save_obj(obj, name ):
    folder=CodeDir+'/obj/'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    with open(folder + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    folder=CodeDir+'/obj/'
    try:
        with open(folder + name + '.pkl', 'rb') as f:
            print name+" remembered!"
            return pickle.load(f)
    except IOError:
        if not os.path.isdir(folder):
            os.makedirs(folder)
        save_obj({},name)
        return {}

def det_fn_name(fn ):
    idx1=str(fn).index('at')
    idx0=str(fn).index(' ')
    return str.strip(str(fn)[idx0:idx1])

def save_workspace():
    for obj in WorkspaceObjects:
        print "Saving %s ..." % obj
        globals()[obj].make_memory()
    print "Done!"

def clear_workspace():
    for obj in WorkspaceObjects:
        print "Clearing %s ..." % obj
        globals()[obj].forget()
    print "Done!"

def clean_slate():
    for obj in WorkspaceObjects:
        print "Clearing %s ..." % obj
        globals()[obj].forget()
    print "Done!"

# Opening and closing these files to get info will take time.
# We can memorize the queries to speed things up as the analysis proceeds.
class memorize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
        self.fn_name=det_fn_name(fn)
        self.remember()
        WorkspaceObjects.append(self.fn_name)
    def __call__(self, *args):
        if args not in self.memo:
	    self.memo[args] = self.fn(*args)
        return self.memo[args]
    def make_memory(self):
        save_obj(self.memo,self.fn_name)
    def remember(self):
        self.memo=load_obj(self.fn_name)
    def forget(self):
        self.memo={}

def date_to_int(NYT_date):
    YEAR=NYT_date[0:4]
    MONTH=NYT_date[5:7]
    DAY=NYT_date[8:10]
    return int(YEAR)*1e4+int(MONTH)*1e2+int(DAY)

def date_to_days(NYT_date):
    try:
        YEAR=NYT_date[0:4]
        MONTH=NYT_date[5:7]
        DAY=NYT_date[8:10]
        return int(YEAR)*365+(int(MONTH)-1)*30+int(DAY)
    except TypeError:
        return 0

def gather_available_files():
    JSON_files=[]
    for file in os.listdir(CodeDir+"/JSON"):
        if file.endswith(".json"):
            JSON_files.append(file)
    return JSON_files

def gather_publication_MY():
    JSON_files=gather_available_files()
    Months=[file[0:file.index('-')] for file in JSON_files]
    Years=[file[file.index('-')+1:file.index('-')+5] for file in JSON_files]
    return (Months,Years)

def run_query(query_list):
    Months,Years=gather_publication_MY()
    query_res={}
    for query in query_list:
        if query[1] is None:
            query_res[query[0]]=[]
        else:
            query_res[query[0]]={query[1]:[]}
        for itr in range(0,len(Years)):
            Year=Years[itr]; Month=Months[itr]
            result=query_archive_all(Month,Year,query[0],query[1])
            if query[1] is None:
                query_res[query[0]]+=result
            else:
                query_res[query[0]][query[1]]+=result
    return query_res

def run_query_matched_idx(query_list):
    Months,Years=gather_publication_MY()
    # Initiallize the output dictionary
    query_res={}
    for query in query_list:
        if query[1] is None:
            query_res[query[0]]=[]
        else:
            query_res[query[0]]={query[1]:[]}

    # Iterate over the years and months
    for itr in range(0,len(Years)):
        Year=Years[itr]; Month=Months[itr]
        query_res_temp={}
        Shortest=-1
        for query in query_list:
            if query[1] is None:
                query_res_temp[query[0]]=[]
            else:
                query_res_temp[query[0]]={query[1]:[]}
            result=query_archive_all(Month,Year,query[0],query[1])
            if Shortest==-1:
                Shortest=len(result)
            if len(result)<Shortest:
                Shortest=len(result)
            if query[1] is None:
                query_res_temp[query[0]]+=result
            else:
                query_res_temp[query[0]][query[1]]+=result

        # We need to match the indeces
        for query in query_list:
            if query[1] is None:
                result=query_res_temp[query[0]]
                query_res[query[0]]+=result[0:Shortest]
            else:
                result=query_res_temp[query[0]][query[1]]
                query_res[query[0]][query[1]]+=result[0:Shortest]

    return query_res

@memorize
def query_archive_all(Month,Year,Field,Subfield=None):
    NArticles=query_article_number(Month,Year)
    result=[]
    LoadFile="/%s-%s.json" % (Month,Year)
    JSONDictionary = json.load(open(JSONDir+LoadFile))
    for Idx in range(0,NArticles):
        try:
            result.append(read_NYTimes(JSONDictionary,Field,Subfield,Idx))
        except Exception as e:
            print "Month %s Year %s Field %s Subfield %s Index %d" % (Month,Year,Field,Subfield,Idx)
            raise e
    return result

@memorize
def query_archive_entry(Month,Year,Field,Subfield=None,Idx=0):
    LoadFile="/%s-%s.json" % (Month,Year)
    JSONDictionary = json.load(open(JSONDir+LoadFile))
    return read_NYTimes(JSONDictionary,Field,Subfield,Idx)

def read_NYTimes(JSONDictionary,Field,Subfield=None,Idx=0):
    try:
        if Subfield is None:
            return JSONDictionary['response']['docs'][Idx][Field]
        else:
            return JSONDictionary['response']['docs'][Idx][Field][Subfield]
    except (IndexError, KeyError, TypeError) as e:
        # print str(e)+' ... continuing'
        if str(e)!='list index out of range' and type(e).__name__!='KeyError' and str(e)!='list indices must be integers, not str':
            raise e
        return None

@memorize
def query_article_number(Month,Year):
    LoadFile="/%s-%s.json" % (Month,Year)
    JSONDictionary = json.load(open(JSONDir+LoadFile))

    try:
        return JSONDictionary['response']['meta']['hits']
    except KeyError as e:
        if str(e)!='\'response\'':
            raise e
        return 0

@memorize
def field_reminder(Month=1,Year=2017):
    LoadFile="/%s-%s.json" % (Month,Year)
    JSONDictionary = json.load(open(JSONDir+LoadFile))
    return JSONDictionary['response']['docs'][0].keys()

@memorize
def subfield_reminder(field,Month=1,Year=2017):
    LoadFile="/%s-%s.json" % (Month,Year)
    JSONDictionary = json.load(open(JSONDir+LoadFile))
    try:
        return JSONDictionary['response']['docs'][0][field].keys()
    except AttributeError:
        return "No subfields."

def grab_archives(Months,Years,WAITTIME=6):
    if not os.path.isfile('archives.out'):
        os.system('echo \' \' > archives.out')

    try:
        for itr in range(0,len(Years)):
            year=Years[itr]
            month=Months[itr]
            # Test if the JSON file exists, if not, submit to NYTimes API in at max 5s intervals
            JSONDir="/home/mrware/Dropbox/Code/NYTimes API/JSON"
            fname='%s/%s-%s.json'%(JSONDir,month,year)
            print fname
            if not os.path.isfile(fname):
                print '%s-%s does not exist, calling API' % (month,year)
                os.system('ruby \'%s/grab_archives.rb\' %s %s >> archives.out'%(CodeDir,month,year))
                print("Waiting %d seconds ..."%WAITTIME)
                time.sleep(WAITTIME)
            else:
                print '%s-%s exists, continuing' % (month,year)
    except IndexError:
        year=Years
        month=Months
        # Test if the JSON file exists, if not, submit to NYTimes API in at max 5s intervals
        JSONDir="/home/mrware/Dropbox/Code/NYTimes API/JSON"
        fname='%s/%s-%s.json'%(JSONDir,month,year)
        print fname
        if not os.path.isfile(fname):
            print '%s-%s does not exist, calling API' % (month,year)
            os.system('ruby \'%s/grab_archives.rb\' %s %s >> archives.out'%(CodeDir,month,year))
            print("Waiting %d seconds ..."%WAITTIME)
            time.sleep(WAITTIME)
        else:
            print '%s-%s exists, continuing' % (month,year)

    print("Done!")

def grab_range_of_archives(Month,Year1=1853,Year2=2018):
    for Year in range(Year1,Year2):
        grab_archives([str(Month)],[str(Year)])

def grab_all_archives():
    for Year in range(2017,1853,-1):
        for Month in range(1,12):
            grab_archives([str(Month)],[str(Year)])
