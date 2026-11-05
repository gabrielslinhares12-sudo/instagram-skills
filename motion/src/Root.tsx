import React from 'react';
import {Composition} from 'remotion';
import {Film} from './Film';
import {episodeSchema,totalFrames,FPS} from './schema';
import demo from '../examples/demo.json';
const defaults=episodeSchema.parse(demo);
export const Root:React.FC=()=> <Composition id="TUEMotion" component={Film} width={2160} height={3840} fps={FPS} durationInFrames={totalFrames(defaults)} defaultProps={defaults} calculateMetadata={({props})=>{const parsed=episodeSchema.parse(props);return {durationInFrames:totalFrames(parsed),props:parsed};}}/>;
