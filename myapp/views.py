from django.shortcuts import redirect, render
from .forms import DVHDumpForm
from scipy.interpolate import interp1d

def index(request):
    if request.method == "POST":
        form = DVHDumpForm(request.POST)
        if form.is_valid():
            dvh_data = analyse_dvh(form.data['dump'])
            return render(request, 'myapp/view_dvh.html', {'dvh_data':dvh_data})
    else:
        form = DVHDumpForm()
    return render(request, 'myapp/index.html', {'form': form})

# def view_dvh(request, dvh_data):
#     return render(request, 'myapp/view_dvh.html',{'dvh_data': dvh_data})

def analyse_dvh(input_data):
    raw_ROIs = input_data.split('ROI')
    prescription = 7.1
    ROI_dict = {}
    for ROI in raw_ROIs[2:]:
        temp_dict = {}
        temp_dict['bin'] = []
        temp_dict['dose'] = []
        temp_dict['volume'] = []
        for i in range(len(ROI.split('\n')[4:-3])):
            temp_dict['bin'].append(int(ROI.split('\n')[4:-3][i].split('\t')[0]))
            temp_dict['dose'].append(float(ROI.split('\n')[4:-3][i].split('\t')[1]))
            temp_dict['volume'].append(float(ROI.split('\n')[4:-3][i].split('\t')[2]))
        temp_dict['volume_cc'] = round(float(temp_dict['volume'][0]),2)
        ROI_dict[ROI.split('***')[0].split('\n')[0][2:].split('\r')[0]] = temp_dict
    for ROI in ROI_dict:
        # import ipdb; ipdb.set_trace()
        f = interp1d(ROI_dict[ROI]['volume'],ROI_dict[ROI]['dose'])
        try:
            ROI_dict[ROI]['D2cc'] = round(float(f(2)),2)
        except:
            pass
        try:
            ROI_dict[ROI]['D90'] = round(float(f(0.9*ROI_dict[ROI]['volume_cc'])),2)
        except:
            pass
        f = interp1d(ROI_dict[ROI]['dose'],ROI_dict[ROI]['volume'])
        try:
            ROI_dict[ROI]['V100'] = round(float(100*(f(prescription)/ROI_dict[ROI]['volume_cc'])),2)
        except:
            pass
        try:
            ROI_dict[ROI]['V67'] = round(float(100*(f(0.67*prescription)/ROI_dict[ROI]['volume_cc'])),2)
        except:
            pass
    ROI_dict['patient_name'] = raw_ROIs[0].split('\r')[0].split('Patient: ')[1]
    ROI_dict['patient_ID'] = raw_ROIs[0].split('\r')[1].split('Patient Id: ')[1]
    ROI_dict['case_label'] = raw_ROIs[0].split('\r')[2].split('Case: ')[1]
    ROI_dict['plan_name'] = raw_ROIs[0].split('\r')[3].split('Plan: ')[1]
    return ROI_dict
