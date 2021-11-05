#!/usr/bin/env python3

import DaVinciResolveScript as dvr_script
import sys
import os

# Give names for the regions
# Names are currently designed to be in alphabetical order
def getAmqRegionName(time):
    if time < 7:
        return "Asia"
    elif time < 15:
        return "Central"
    else:
        return "Western"
  
def processVideos(project_name, file, region):
    resolve = dvr_script.scriptapp('Resolve')
    pm = resolve.GetProjectManager()
    proj = pm.CreateProject(project_name)

    if not proj:
        print("Unable to create project " + project_name)
        return

    proj.SetSetting('timelineFrameRate', "60")
    proj.SetSetting("timelineResolutionWidth", "1280")
    proj.SetSetting("timelineResolutionHeight", "720")

    mediaPool = proj.GetMediaPool()
    mediaStorage = resolve.GetMediaStorage()
    clips = mediaStorage.AddItemListToMediaPool(file)
    timeline_name = "Timeline 1"
    timeline = mediaPool.CreateEmptyTimeline(timeline_name)
    mediaPool.AppendToTimeline(clips[0])

    # Get MarkIn and MarkOut
    mark_out = timeline.GetEndFrame() - (60 * 30) 
    mark_in = timeline.GetStartFrame() + (60 * 100) 

    render_settings = {"MarkIn":mark_in, "MarkOut":mark_out, "TargetDir":"location", "CustomName":project_name}
    proj.LoadRenderPreset('AMQ 720P')
    proj.SetRenderSettings(render_settings)
    proj.DeleteAllRenderJobs()
    proj.AddRenderJob()
    
videoFolderLocation = "location2"
files = os.listdir(videoFolderLocation)
for f in files:
    # Look through all the files in the designated folder
    # Use the video name to figure out the variables for the project
    videoParams = f.replace('.',' ').split(' ')
    videoDate = videoParams[0]
    time = int(videoParams[1].split('-')[0])
    region = getAmqRegionName(time)
    projectName = "Ranked " + videoDate + " " + region
    fileLocation = videoFolderLocation + "\\" + f
    processVideos(projectName, fileLocation, region)
